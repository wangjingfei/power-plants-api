from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    isActive: Optional[bool] = True

class UserCreate(UserBase):
    name: str
    email: EmailStr

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass 