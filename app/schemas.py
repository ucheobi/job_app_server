from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Role(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"

class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: Role.JOB_SEEKER
    password: str
    profile_picture: Optional[str]

class UserLogin(BaseModel):
    email: str
    password: str