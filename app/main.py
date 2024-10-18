from fastapi import FastAPI
from app.api.routers import company, job_profile, user, auth
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(job_profile.router)
app.include_router(company.router)
