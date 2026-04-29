from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from .models import User, UserProfile
from .crud import create_user_with_profile, get_user

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserRequest(BaseModel):
    name: str
    bio: str


@app.get("/")
def home():
    return {"message": "Single API One-to-One Project Running"}


@app.post("/users")
def create_user_api(data: UserRequest, db: Session = Depends(get_db)):
    user, profile = create_user_with_profile(db, data.name, data.bio)

    return {
        "message": "User and Profile created successfully",
        "user": {
            "id": user.id,
            "name": user.name
        },
        "profile": {
            "id": profile.id,
            "bio": profile.bio
        }
    }


@app.get("/users/{user_id}")
def get_user_api(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "profile": {
            "id": user.profile.id,
            "bio": user.profile.bio
        } if user.profile else None
    }