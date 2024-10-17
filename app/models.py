from sqlalchemy import  Column, String, Integer, Enum as SqlEnum, ForeignKey, JSON, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
metadata = Base.metadata

class UserRole(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    #An admin can manage all users
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    owner = relationship("User")
    current_location = Column(String, nullable=False)
    title = Column(String, nullable=False)
    resume_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
    
    #Storing skills as List of strings
    skills = Column(JSON, nullable=True)

    #storing Education and work experience as an array of JSON obhjects
    education = Column(JSON, nullable=True)
    work_experience = Column(JSON, nullable=True)

class CompanySize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class Recruiter(Base):
    __tablename__ = "recruiters"

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