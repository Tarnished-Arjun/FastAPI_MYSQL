from sqlalchemy.orm import Session
from models import Item

def create_item(db: Session, name: str, description: str, price: int):
    item = Item(name=name, description=description, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()