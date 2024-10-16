from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db


router = APIRouter(
    prefix="/profiles",
    tags=['Profiles']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProfileResponse)
def create_my_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    _profile = db.query(models.Profile).filter(models.Profile.owner_id == current_user.id).first()
    
    if _profile:
        print("Profile already exist!") #Debbugging purposes
        return _profile

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

@router.get("/", response_model=schemas.Profile)
def get_my_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    profile  = db.query(models.Profile).filter(models.Profile.owner_id == current_user.id).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile found, add your profile!")

    return profile

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_profile(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    profile_query = db.query(models.Profile).filter(models.Profile.owner_id == current_user.id)

    profile = profile_query.first()

    if profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have any job profile yet!!!")
    
    profile_query.delete()
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/")
def update_my_profile(profile_update: schemas.ProfileCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    profile_query = db.query(models.Profile).filter(models.Profile.owner_id == current_user.id)
    profile = profile_query.first()

    if not profile:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile exist for current user, please add your job profile!!!")
    
    profile_query.update(profile_update.model_dump(), synchronize_session=False)
    db.commit()

    return profile