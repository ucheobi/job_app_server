import os
from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.utils import save_resume_file
from ... import schemas, models, oauth2
from ...database import get_db
import json


router = APIRouter(
    prefix="/applicants",
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

    #Check if user already has a profile
    existing_applicant = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id).first()
    
    if existing_applicant:
        return existing_applicant

    #Parse JSON string 
    try:
        applicant_data_dict = json.loads(applicantData)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid json data detected!")

    #Save resume file in local directory
    resume_url = await save_resume_file(resumeFile)
    applicant_data_dict["resume_url"] = resume_url

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


@router.get("/", response_model=schemas.Applicant)
def get_applicant_profile(
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)
    ):

    applicant  = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id).first()

    if not applicant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile found, add your JobSeekerProfile!")

    return applicant


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
def update_applicant_profile(
        applicant_update: schemas.ApplicantCreate, 
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_current_user)
    ):

    applicant_query = db.query(models.Applicant).filter(models.Applicant.owner_id == current_user.id)
    applicant = applicant_query.first()

    if not applicant:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile exist for current user, please add your job profile!!!")
    
    applicant_query.update(applicant_update.model_dump(), synchronize_session=False)
    db.commit()

    return applicant