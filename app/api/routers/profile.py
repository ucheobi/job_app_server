from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db


router = APIRouter(
    prefix="/profiles",
    tags=['Profiles']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas)
def create_job_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    try:
        new_profile = models.Profile(owner_id=current_user.id, **profile.model_dump())
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