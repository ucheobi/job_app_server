from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db


router = APIRouter(
    prefix="/recruiters",
    tags=['Recruiters']
)

# current_user: int = Depends(oauth2.get_current_user)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recruiter_account(recruiter: schemas.RecruiterCreate, db: Session = Depends(get_db)):
    
    try:
        account = models.Recruiter(**recruiter.model_dump())
        db.add(account)
        db.commit()
        db.refresh(account)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail={
                                "message": f"Failed to create recruiter - One or more required fields are missing!",
                                "error": str(e)
                            })
    
    return account