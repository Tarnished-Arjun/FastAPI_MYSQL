from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from crud import create_item, get_item

app = FastAPI()


Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/items")
def create_item_api(
    name: str,
    description: str,
    price: int,
    db: Session = Depends(get_db)
):
    return create_item(db, name, description, price)


@app.get("/items/{item_id}")
def get_item_api(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = get_item(db, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item