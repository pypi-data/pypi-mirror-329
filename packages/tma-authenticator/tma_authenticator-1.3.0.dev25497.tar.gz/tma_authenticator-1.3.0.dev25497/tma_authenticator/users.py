from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: Optional[str] = ''
    username: Optional[str] = ''
    tg_id: int
    tg_language: str = ''  # language_code from TG


class UserDB(User):
    is_service: bool = False
    cache_key: Optional[str] = None