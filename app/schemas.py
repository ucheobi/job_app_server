from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from enum import Enum
from datetime import date, datetime

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
    end_date: str | None = Field(default=None)
    description: str | None = Field(default=None)

class Applicant(BaseModel):
    title: str
    current_location: str
    resume_url: str | None = Field(default=None)
    portfolio_url: str | None = Field(default=None)
    skills: List[str] = []
    education: List[Education] = []
    work_experience: List[WorkExperience] = []

    class Config:
        from_attribute = True

class ApplicantCreate(Applicant):
    pass

class ApplicantResponse(Applicant):
    owner: UserResponse


#Company profile account
class CompanySize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Company(BaseModel):
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

class CompanyCreate(Company):
    pass

class Status(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class JobBase(BaseModel):
    title: str
    description: str
    requirements: str | None = Field(default=None)
    location: str
    job_type: str
    salary_min: float | None = Field(default=None)
    salary_max: float | None = Field(default=None)
    posted_date: date | None = Field(default=None)
    status: Status

    class Config:
        from_attribute = True

class CompanyResponse(Company):
    id: int
    owner: UserResponse
    created_at: datetime
    
    jobs: List[JobBase]


class CustomMessage(BaseModel):
    message: str


class JobCreate(JobBase):
    company_id: int

class JobResponse(JobBase):
    id: int

