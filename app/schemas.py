from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from enum import Enum
from datetime import date


class Role(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"

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

class ResponseToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None =  None

class Education(BaseModel):
    institution: str
    degree: str
    graduation_year: int

class Current(Enum):
    TILL_DATE = "TILL_DATE"

class WorkExperience(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: Optional[str]
    description: Optional[str]

class Profile(BaseModel):
    title: str
    current_location: str
    resume_url: Optional[str]
    portfolio_url: Optional[str]
    skills: Optional[List[str]]
    education: Optional[List[Education]]
    work_experience: Optional[List[WorkExperience]]

    class Config:
        from_attribute = True

class ProfileCreate(Profile):
    pass

class ProfileResponse(Profile):
    owner: UserResponse