from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.routers.applicant import get_applicant_profile
from ... import database, models, schemas, utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.ResponseTokenWithInitialData)
def login(response: Response, user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials!")
    
    is_match = utils.verify_password(user_credential.password, user.password)

    if not is_match:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username or password incorrect!")
        
    applicant = utils.fetch_applicant_profile(db, user.id)
    jobs = utils.fetch_jobs(db)

    # return an access token
    access_token = oauth2.create_access_token(data={
            "user_id": user.id, 
            "email": user.email,
            "role": user.role, 
        }
    )

    response.set_cookie(key="user", value=access_token, max_age=600, httponly=True)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "applicant": applicant,
        "jobs": jobs
    }