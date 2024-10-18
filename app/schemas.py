from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

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


#Job seeker profile
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

class JobSeekerProfile(BaseModel):
    title: str
    current_location: str
    resume_url: Optional[str]
    portfolio_url: Optional[str]
    skills: Optional[List[str]]
    education: Optional[List[Education]]
    work_experience: Optional[List[WorkExperience]]

    class Config:
        from_attribute = True

class JobSeekerProfileCreate(JobSeekerProfile):
    pass

class JobSeekerProfileResponse(JobSeekerProfile):
    owner: UserResponse


#Company profile account
class CompanySize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class CompanyProfile(BaseModel):
    company_name: str
    company_website: str | None = Field(default=None)
    company_email: str
    company_size: CompanySize
    industry: str
    company_description: str
    company_logo: str | None = Field(default=None)
    posting_permission: bool = False

    class Config:
        from_attribute = True

class CompanyProfileCreate(CompanyProfile):
    pass

class CompanyProfileResponse(CompanyProfile):
    id: int
    owner: UserResponse