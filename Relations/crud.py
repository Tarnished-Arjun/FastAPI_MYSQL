from sqlalchemy.orm import Session
from .models import User, UserProfile


def create_user(db: Session, name: str):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_profile(db: Session, user_id: int, bio: str):
    profile = UserProfile(user_id=user_id, bio=bio)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_profile(db: Session, profile_id: int):
    return db.query(UserProfile).filter(UserProfile.id == profile_id).first()


def update_profile(db: Session, profile_id: int, bio: str):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if profile:
        profile.bio = bio
        db.commit()
        db.refresh(profile)

    return profile


def delete_profile(db: Session, profile_id: int):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if profile:
        db.delete(profile)
        db.commit()

    return profile