from datetime import date, datetime
from sqlalchemy import  Column, Date, Float, String, Integer, Enum as SqlEnum, ForeignKey, JSON, Boolean, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata

class Role(str, Enum):
    APPLICANT = "applicant"
    EMPLOYER = "employer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    owner = relationship("User")
    current_location = Column(String, nullable=False)
    title = Column(String, nullable=False)
    resume_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    applications = relationship("JobApplication", back_populates="applicant")
    
    #Storing skills as List of strings
    skills = Column(JSON, nullable=True)

    #storing Education and work experience as an array of JSON obhjects
    education = Column(JSON, nullable=True)
    work_experience = Column(JSON, nullable=True)

class CompanySize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, nullable=False)
    company_name = Column(String, nullable=False)
    company_website = Column(String, nullable=True)
    company_email = Column(String, nullable=False, unique=True)
    company_size = Column(SqlEnum(CompanySize), nullable=False)
    industry = Column(String, nullable=False)
    company_description = Column(String, nullable=False)
    company_logo = Column(String, nullable=True)
    posting_permission = Column(Boolean, server_default="FALSE", nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    jobs = relationship("Job", back_populates="company")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    owner = relationship("User")

class Status(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    job_type = Column(String(50), nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    posted_date = Column(Date, default=date.today)
    status = Column(SqlEnum(Status), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="jobs")
    applicants = relationship("JobApplication", back_populates="job")

class ApplicationStatus(str, Enum):
    PENDING = "Pending"
    REVIEWED = "Reviewed"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, nullable=False)
    job_applicant_id = Column(Integer, ForeignKey("applicants.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    application_date = Column(Date, default=date.today)
    application_status = Column(SqlEnum(ApplicationStatus), default=ApplicationStatus.PENDING)
    resume_file = Column(String, nullable=True)

    job =  relationship("Job", back_populates="applicants")
    applicant = relationship("Applicant", back_populates="applications")