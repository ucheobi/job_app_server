from fastapi import FastAPI
from app.api.routers import applicant, company, user, auth, job
from . import models, database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(applicant.router)
app.include_router(company.router)
app.include_router(job.router)
