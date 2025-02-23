import base64
import json
import hashlib
import hmac
from typing import List, TypeVar, Callable, Optional
from aiocache import cached, caches # type: ignore
from urllib.parse import unquote
from fastapi import HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from pydantic import BaseModel
import httpx
from jose import jwt
from .users import User, UserDB
from .storage_provider import StorageProvider
from .tma_authentication_router import TMAAuthenticationRouter


T = TypeVar('T', bound=BaseModel)

class TMAAuthenticator:
    bot_token: str
    auth_url: str
    storage_provider: StorageProvider
    authentication_router: TMAAuthenticationRouter
    user_model: Callable[..., T]

    def __init__(self,
                 service_name: str,
                 bot_token: str,
                 auth_url: str,
                 storage_provider: StorageProvider,
                 user_model: Optional[Callable[..., T]] = None):
        self.service_name = service_name
        self.bot_token = bot_token
        self.auth_url = auth_url
        self.storage_provider = storage_provider
        self.authenticator_router_provider = TMAAuthenticationRouter(
            auth_url=self.auth_url,
            storage_provider=self.storage_provider
        )
        self.user_model = user_model or UserDB # type: ignore
        self._s2s_certificates = None  # Will hold JWKS data once loaded
        self.httpx_client = httpx.AsyncClient()

    async def load_s2s_certificates(self) -> dict:
        """
        Fetches JWKS data once and caches it in self._s2s_certificates.
        If it's already loaded, just return it.
        """
        if self._s2s_certificates is None:
            resp = await self.httpx_client.get(f"{self.auth_url}/.well-known/jwks.json")
            resp.raise_for_status()
            self._s2s_certificates = resp.json()
        return self._s2s_certificates # type: ignore

    @property # type: ignore
    def authentication_router(self): # type: ignore
        return self.authenticator_router_provider

    async def oauth_verify_token(
            self,
            x_service_token: Optional[str] = Security(APIKeyHeader(name="X-Service-Token", auto_error=False)),
            authorization: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)),
            # authorization=Security(APIKeyHeader(name="Authorization")), or /
    ):
        return await self.verify_token(
            authorization=authorization,
            x_service_token=x_service_token
        )


    async def refresh_user_cache(self, cache_key: str):
        """
        Invalidates the cached verify_token result for the given authorization and optional extra_tokens_validation.
        Call this method after updating the user's data to force cache renewal.
        """

        # Delete the cache entry so the next token verification will recompute and refresh the user data.
        cache = caches.get('default')
        await cache.delete(cache_key)

    @cached(
        key_builder=lambda f, *args,
                           **kwargs: f"{kwargs.get('authorization') or kwargs.get('x_service_token')}:{hashlib.sha256(json.dumps(kwargs.get('extra_tokens_validation') or []).encode()).hexdigest()}",
        ttl=300,
        alias="default"
    )
    async def verify_token(self,
                           authorization: Optional[str] = None,
                           x_service_token: Optional[str] = None,
                           extra_tokens_validation: Optional[List[str]] = None) -> T:
        user = None
        update_user_attributes = False
        is_service: bool
        if authorization:
            is_service = False
            try:
                decoded_bytes = base64.b64decode(authorization)
                decoded_data = json.loads(decoded_bytes.decode('utf-8'))
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"You are not authorized to access this resource: {e}")

            user = User(**decoded_data)
            valid = self.is_valid_user_info(
                web_app_data=decoded_data['initData'],
                bot_token=self.bot_token,
                extra_tokens_validation=extra_tokens_validation
            )
            if not valid:
                raise HTTPException(status_code=401,
                                    detail="Invalid credentials.",
                                    headers={"Authorization": "Bearer"})
            user_data = self.get_user_data_dict(decoded_data['initData'])
            user.tg_language = user_data.get("language_code", "en")
            update_user_attributes = True
        elif x_service_token:
            """
            Token must have scope with 'user:<TG_ID>' and '{SERVICE_NAME}',
            to provide access to all services, scope must have ['user:<TG_ID>', 'admin'] 
            """
            is_service = True
            jwks_data = await self.load_s2s_certificates()
            x_service_token = x_service_token.replace("Bearer ", "")
            try:
                x_service_token_decoded = jwt.decode(x_service_token, jwks_data, options={
                    "verify_aud": False,
                    "verify_iss": False,
                })
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"You are not authorized to access this resource: {e}")
            scope = x_service_token_decoded.get("scope", [])
            if self.service_name not in scope and "admin" not in scope:
                raise HTTPException(
                    status_code=401,
                    detail=f"You are not authorized to access {self.service_name}. Scope: {scope}."
                )

            for scope in scope:
                if "user" in scope:
                    tg_id = int(scope.split("user:")[1])
                    user = User(
                        tg_id=tg_id,
                        first_name="Service",
                        last_name=f"User {tg_id}",
                        username=f"service_user_{tg_id}",
                        tg_language="en"
                    )
            if not user:
                raise HTTPException(status_code=401, detail="You are not authorized to access this resource.")
        else:
            raise ValueError("Either 'authorization' or 'x_service_token' must be provided.")

        cache_key = f"{authorization or x_service_token}:{hashlib.sha256(json.dumps(extra_tokens_validation or []).encode()).hexdigest()}"

        db_user = await self.storage_provider.retrieve_user(search_query={'tg_id': user.tg_id})
        if not db_user:
            insert_id = await self.storage_provider.insert_user(
                user_data=user.model_dump()
            )
            return self.user_model(
                id=str(insert_id),
                **user.model_dump(),
                cache_key=cache_key,
                is_service=is_service
            )
        elif update_user_attributes:
            attributes_to_compare = ['tg_language', 'first_name', 'last_name', 'username']
            for attr in attributes_to_compare:
                if getattr(user, attr) != db_user.get(attr):
                    await self.storage_provider.update_user(
                        id=db_user['id'],
                        update_data={
                            'tg_language': user.tg_language,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'username': user.username
                        }
                    )
                    break
            return self.user_model(**db_user, cache_key=cache_key, is_service=is_service)
        else:
            return self.user_model(**db_user, is_service=is_service)

    def is_valid_user_info(self,
                           web_app_data,
                           bot_token: str,
                           extra_tokens_validation: Optional[List[str]] = None
    ) -> bool:
        try:
            data_check_string = unquote(web_app_data)
            data_check_arr = data_check_string.split('&')
            needle = 'hash='
            hash_item = next((item for item in data_check_arr if item.startswith(needle)), '')
            tg_hash = hash_item[len(needle):]
            data_check_arr.remove(hash_item)
            data_check_arr.sort()
            data_check_string = "\n".join(data_check_arr)
            secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
            calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

            if calculated_hash != tg_hash:
                if extra_tokens_validation:
                    for token in extra_tokens_validation:
                        valid = self.is_valid_user_info(web_app_data=web_app_data, bot_token=token)
                        if valid:
                            return True
                return False
        except Exception as e:
            return False
        return True


    def get_user_data_dict(self, user_init_data: str) -> dict:
        unquote_user_data = unquote(user_init_data)

        start_index_value = 'user='
        end_index_value = '&chat_instance=' if 'start_param' in unquote_user_data else '&auth_date='

        start_index = unquote_user_data.find(start_index_value) + len(start_index_value)
        end_index = unquote_user_data.find(end_index_value)
        user_data_string = unquote_user_data[start_index:end_index]
        return json.loads(user_data_string)
