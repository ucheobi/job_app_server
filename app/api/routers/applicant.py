from typing import List, Literal
from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.utils import fetch_applicant_profile
from ... import schemas, models, oauth2
from ...database import get_db
import json


router = APIRouter(
    prefix="/applicant",
    tags=['Applicants']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ApplicantResponse)
async def create_applicant_profile(
        applicantData: str = Form(...), 
        resumeFile: UploadFile = File(...),
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)
    ):

    #ToDo - Make an admin also create a job profile for user and attach owner of the profile

    if current_user.role == "employer":
        print("You are not authorized")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    #Check if user already has a profile and return it
    existing_applicant = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id).first()
    
    if existing_applicant:
        return existing_applicant

    #Parse JSON string 
    try:
        applicant_data_dict = json.loads(applicantData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid json data detected!")

    #Save resume file in local directory
    #await save_resume_file(resumeFile)
    if resumeFile and resumeFile.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code="401", detail="Only pdf or doc/docx files are allowed!")

    if resumeFile:
        binary_content = await resumeFile.read()

        applicant_data_dict["resume"] = binary_content
        applicant_data_dict["resume_url"] = resumeFile.filename

    try:
        new_applicant = models.Applicant(owner_id=current_user.id, **applicant_data_dict)
        db.add(new_applicant)
        db.commit()
        db.refresh(new_applicant)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail={
                                "message": f"Failed to create profile - One or more required fields are missing!",
                                "error": str(e)
                            })
    return new_applicant


@router.get("/", response_model=schemas.ApplicantResponse | Literal['NO_PROFILE_FOUND'])
def get_applicant_profile(
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)
    ):

    return fetch_applicant_profile(db, current_user.id)


@router.get("/all", response_model=List[schemas.Applicant])
def get_all_applicants(db: Session = Depends(get_db)):
    applicants = db.query(models.Applicant).all()

    return applicants

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_applicant_profile(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_profile_query = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id)

    user_profile = user_profile_query.first()

    if user_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have any profile yet!!!")
    
    user_profile_query.delete()
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=schemas.ApplicantResponse)
async def update_applicant_profile(
        applicantData: str = Form(...),
        resumeFile: UploadFile = None,
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)
    ):

    applicant_query = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id)
    applicant = applicant_query.first()

    if not applicant:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile exist for current user, please add your job profile!!!")
    
    #Parse JSON string 
    try:
        applicant_data_dict = json.loads(applicantData)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid json data detected!")
    
    if resumeFile and resumeFile.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code="401", detail="Only pdf or doc/docx files are allowed!")

    if resumeFile:
        binary_content = await resumeFile.read()

        applicant_data_dict["resume"] = binary_content
        applicant_data_dict["resume_url"] = resumeFile.filename
    
    try:
        applicant_query.update(applicant_data_dict, synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail={
                                "message": f"Failed to Update profile",
                                "error": str(e)
                            })

    return applicant