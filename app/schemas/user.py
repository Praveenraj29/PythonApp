from typing import Optional, Union

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserCreateOpen(BaseModel):
    email: EmailStr
    password: str
    full_name: Union[str, None] = None

class UserOut(UserBase):
    id: int


