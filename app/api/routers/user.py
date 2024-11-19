from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from ... import schemas, models, utils, oauth2
from ...database import get_db
from typing import List


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseToken)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    _user = db.query(models.User).filter(models.User.email == user.email).first()

    if _user and _user.email == user.email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {_user.email} already exist. Sign in to your account!!!")
    
    user.password = utils.get_password_hash(user.password)
    
    new_user = models.User(**user.model_dump())

    # send a token
    token = oauth2.create_access_token(data={
        "user_id": new_user.id, 
        "role": new_user.role, 
        "email": user.email, 
        "first_name": user.first_name, 
        "last_name": user.last_name
        }
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail={
                    "message": f"Failed to create user, something went wrong!!!",
                    "error": str(e)
                }
            )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users

@router.delete("/{user_id}")
def delete_user(
        user_id: int, 
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ):

    if not current_user:
        return Response(content="You are not authorized", status_code=status.HTTP_401_UNAUTHORIZED)
    
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id of {user_id} does not exist!!!")
    
    user_query.delete()
    db.commit()

    return schemas.CustomMessage(message="User successfully deleted")