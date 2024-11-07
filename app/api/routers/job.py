from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ... import schemas, models, oauth2
from ...database import get_db
from typing import List

router = APIRouter(
    prefix="/jobs",
    tags=["Job"]
)

@router.post("/")
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    
    if current_user.role == "applicant":
        return Response(content="You are not authorized", status_code=status.HTTP_401_UNAUTHORIZED)
      
    try:
        new_job = models.Job(**job.model_dump())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail={
                                "message": f"Failed to create job - One or more required fields are missing!",
                                "error": str(e)
                            })
    return new_job

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job :
        raise HTTPException(status_code=404, detail="This job is no longer available!!")
    
    return job


@router.get("/", response_model=List[schemas.JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()

    return jobs

@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(
        job_id: int, 
        job_data: schemas.JobCreate, 
        db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_current_user)
     ):
    
    if current_user.role == "applicant":
        return Response(content="You are not authorized", status_code=status.HTTP_401_UNAUTHORIZED)
    
    job_query = db.query(models.Job).filter(models.Job.id == job_id)
    job = job_query.first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"job with id of {job_id} does not exist!!!")
    
    job_dict = job_data.model_dump()
    job_query.update(job_dict, synchronize_session=False)

    db.commit()

    return job_query.first()

@router.delete("/{job_id}")
def delete_job(
        job_id: int, 
        db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)
    ):

    if current_user.role == "applicant":
        return Response(content="You are not authorized", status_code=status.HTTP_401_UNAUTHORIZED)
    
    job_query = db.query(models.Job).filter(models.Job.id == job_id)
    job = job_query.first()

    if job == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"job with id of {job_id} does not exist!!!")
    
    job_query.delete()
    db.commit()

    return schemas.CustomMessage(message="Job successfully deleted")
    