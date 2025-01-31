from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db


router = APIRouter(
    prefix="/company",
    tags=['Company']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CompanyResponse)
def create_company_profile(
        recruiter: schemas.CompanyCreate, 
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    #Verify role of user
    if current_user.role == "applicant":
        return Response(content="You are not authorized", status_code=status.HTTP_401_UNAUTHORIZED)

    _account = db.query(models.Company).filter(models.Company.owner_id == current_user.id).first()

    #Check if company already has an account
    if _account:
        print("An account already existed")
        return _account
    
    try:
        account = models.Company(owner_id=current_user.id,**recruiter.model_dump())
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


@router.get("/", response_model=schemas.CompanyResponse)
def get_company_profile(
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    #Verify role of user
    if current_user.role == "applicant":
        print("You are not authorized")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    company_data  = db.query(models.Company).filter(models.Company.owner_id == current_user.id).first()

    if not company_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No profile found, add your company profile!")

    return company_data


@router.put("/", response_model=schemas.CompanyResponse)
def update_company_profile(
        new_profile_details: schemas.CompanyCreate, 
        db: Session = Depends(get_db), 
        current_user: int = Depends(oauth2.get_current_user)
    ):

    #Verify role of user
    if current_user.role != "employer": #only company should update profile here
        print("You are not authorized")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    account_query = db.query(models.Company).filter(models.Company.owner_id == current_user.id)
    account = account_query.first()

    if not account:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No company profile found!!")
    
    account_query.update(new_profile_details.model_dump(), synchronize_session=False)
    db.commit()

    return account


@router.delete("/", response_model=schemas.CustomMessage)
def delete_account_profile(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

     #Verify role of user
    if current_user.role != "admin": # only admin should delete company profile
        return schemas.CustomMessage(message="You are not authorized! Please contact the admin")
    
    account_query = db.query(models.Company).filter(models.Company.owner_id == current_user.id)

    account = account_query.first()

    if account == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have any job profile yet!!!")
    
    
    account_query.delete()
    db.commit()
    
    return schemas.CustomMessage(message="Account successfully deleted")