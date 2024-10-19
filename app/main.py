from fastapi import FastAPI
from app.api.routers import applicant, company, user, auth, job
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(applicant.router)
app.include_router(company.router)
app.include_router(job.router)
