import bcrypt
from fastapi import HTTPException, UploadFile
import os
from dotenv import load_dotenv

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
    