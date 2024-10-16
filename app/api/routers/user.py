from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ... import schemas, models, utils
from ...database import get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserRegistration, db: Session = Depends(get_db)):
    _user = db.query(models.User).filter(models.User.email == user.email).first()

    if _user and _user.email == user.email:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"user with email: {_user.email} already exist!!!")
    
    user.password = utils.get_password_hash(user.password)
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users