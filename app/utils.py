import bcrypt
from fastapi import Depends, HTTPException, UploadFile
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

load_dotenv()

DIRECTORY_PATH = os.getenv("DIRECTORY_PATH")

def get_password_hash(password: str) -> str:
    pwd_bytes  = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt).decode('utf-8')
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_encode = plain_password.encode('utf-8')

    verify = bcrypt.checkpw(password=password_byte_encode, hashed_password=hashed_password.encode('utf-8'))
    return verify

async def save_resume_file(resume_file: UploadFile) -> str:

    file_location = f"{DIRECTORY_PATH}/{resume_file.filename}"

     #validate type of file
    if resume_file:
        if resume_file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(status_code="401", detail="Only pdf or doc/docx files are allowed!")

    try:
        #Save the file locally
        with open(file_location, "wb") as file:
            file_content = await resume_file.read()
            file.write(file_content)

        return file_location
    except Exception as e:
        raise HTTPException(status_code="402", detail="Error while saving file!")
    
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job :
        raise HTTPException(status_code=404, detail="This job is no longer available!!")
    
    return job