from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import SessionDep
from ... import schemas, models

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/")
def get_users(db: SessionDep):
    users = db.query(models.User).all()

    return users