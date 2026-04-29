from sqlalchemy.orm import Session
from .models import User, UserProfile


def create_user_with_profile(db: Session, name: str, bio: str):
    user = User(name=name)

    profile = UserProfile(bio=bio)

    user.profile = profile

    db.add(user)
    db.commit()

    db.refresh(user)
    db.refresh(profile)

    return user, profile


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    print(user.profile)
    return user


def update_user_with_profile(db: Session, user_id: int, name: str, bio: str):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        user.name = name

        if user.profile:
            user.profile.bio = bio

        db.commit()
        db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        if user.profile:
            db.delete(user.profile)

        db.delete(user)
        db.commit()

    return user