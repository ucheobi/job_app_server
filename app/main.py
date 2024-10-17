from fastapi import FastAPI
from app.api.routers import profile, user, auth, recruiter
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(recruiter.router)
