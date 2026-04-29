from sqlalchemy.orm import Session
from .models import User, UserProfile


def create_user_with_profile(db: Session, name: str, bio: str):
    user = User(name=name)

    db.add(user)
    db.commit()
    db.refresh(user)

    profile = UserProfile(
        bio=bio,
        user_id=user.id
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return user, profile


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()