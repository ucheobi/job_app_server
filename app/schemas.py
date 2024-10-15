from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserRegistration(UserBase):
    first_name: str
    last_name: str
    role: Role

class UserLogin(BaseModel):
    pass

class UserResponse(UserRegistration):
    id: int
    password: str = Field(exclude=True)
    
    class Config:
        from_attribute = True