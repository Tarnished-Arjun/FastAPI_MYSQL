from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User, UserProfile
from .database import SessionLocal, engine, Base
from .crud import (
    create_user,
    create_profile,
    get_user,
    get_profile,
    update_profile,
    delete_profile
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "One-to-One Relationship Running"}


@app.post("/users")
def create_user_api(name: str, db: Session = Depends(get_db)):
    return create_user(db, name)


@app.post("/profiles")
def create_profile_api(
    user_id: int,
    bio: str,
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    return create_profile(db, user_id, bio)


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


@app.get("/profiles/{profile_id}")
def get_profile_api(profile_id: int, db: Session = Depends(get_db)):
    profile = get_profile(db, profile_id)

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "id": profile.id,
        "bio": profile.bio,
        "user": {
            "id": profile.user.id,
            "name": profile.user.name
        }
    }


@app.put("/profiles/{profile_id}")
def update_profile_api(
    profile_id: int,
    bio: str,
    db: Session = Depends(get_db)
):
    profile = update_profile(db, profile_id, bio)

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@app.delete("/profiles/{profile_id}")
def delete_profile_api(profile_id: int, db: Session = Depends(get_db)):
    profile = delete_profile(db, profile_id)

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {"message": "Profile deleted successfully"}