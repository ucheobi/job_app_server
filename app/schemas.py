from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from enum import Enum
from datetime import date, datetime

class Role(str, Enum):
    APPLICANT = "applicant"
    EMPLOYER = "employer"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)

class UserCreate(UserBase):
    first_name: str
    last_name: str
    role: Role

class UserLogin(BaseModel):
    pass

class UserResponse(UserCreate):
    id: int
    password: str = Field(exclude=True)

    class Config:
        from_attribute = True

class ResponseToken(BaseModel):
    access_token: str
    token_type: str

class UserResponseWithToken(BaseModel):
    access_token: str
    user: UserResponse

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
    resume_url: str
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
    required_skills:  List[str] = []
    technologies: List[str] = []
    location: str
    job_type: str
    salary_min: float | None = Field(default=None)
    salary_max: float | None = Field(default=None)
    posted_date: date | None = Field(default=None)
    status: Status
    other_details: str | None = Field(default=None)
    our_offers: str | None = Field(default=None)

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
    company: Company

class ResponseTokenWithInitialData(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class JobApplicationBase(BaseModel):
    job_applicant_id: int
    job_id: int
    application_date: Optional[date] = date.today()
    application_status: Optional[ApplicationStatus] = ApplicationStatus.PENDING
    resume_file: Optional[str]

class JobApplicationCreate(BaseModel):
    job_id: int

class JobApplicationUpdate(BaseModel):
    application_status: Optional[ApplicationStatus]

class JobApplicationResponse(JobApplicationBase):
    id: int

    class Config:
        orm_mode: True