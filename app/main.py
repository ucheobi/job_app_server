from fastapi import FastAPI
from app.api.routers import user, auth
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def test():
    return "Hello world"