from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db


router = APIRouter(
    prefix="/job_profiles",
    tags=['Job_Profiles']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.JobSeekerProfileResponse)
def create_job_profile(
        profile: schemas.JobSeekerProfileCreate, 
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    #ToDo - Make an admin also create a job profile for user and attach owner of the profile
    if current_user.role == "employer":
        print("You are not authorized")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    _profile = db.query(models.JobSeekerProfile).filter(models.JobSeekerProfile.owner_id == current_user.id).first()
    
    if _profile:
        return _profile

    try:
        new_profile = models.JobSeekerProfile(owner_id=current_user.id, **profile.model_dump())
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail={
                                "message": f"Failed to create profile - One or more required fields are missing!",
                                "error": str(e)
                            })
    return new_profile


@router.get("/", response_model=schemas.JobSeekerProfile)
def get_job_profile(
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    user_profile  = db.query(models.JobSeekerProfile).filter(models.JobSeekerProfile.owner_id == current_user.id).first()

    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No JobSeekerProfile found, add your JobSeekerProfile!")

    return user_profile


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_profile_query = db.query(models.JobSeekerProfile).filter(models.JobSeekerProfile.owner_id == current_user.id)

    user_profile = user_profile_query.first()

    if user_profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have any job profile yet!!!")
    
    user_profile_query.delete()
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/", response_model=schemas.JobSeekerProfileResponse)
def update_my_profile(
        profile_update: schemas.JobSeekerProfileCreate, 
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    user_profile_query = db.query(models.JobSeekerProfile).filter(models.JobSeekerProfile.owner_id == current_user.id)
    user_profile = user_profile_query.first()

    if not user_profile:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile exist for current user, please add your job profile!!!")
    
    user_profile_query.update(profile_update.model_dump(), synchronize_session=False)
    db.commit()

    return user_profile