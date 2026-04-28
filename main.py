from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from crud import (
    create_item, get_item,
    create_employee, get_all_employees,
    get_employee, update_employee, delete_employee
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
    return {"message": "FastAPI MySQL Running"}


@app.post("/items")
def create_item_api(
    name: str,
    description: str,
    price: int,
    db: Session = Depends(get_db)
):
    return create_item(db, name, description, price)


@app.get("/items/{item_id}")
def get_item_api(item_id: int, db: Session = Depends(get_db)):
    item = get_item(db, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item



@app.post("/employees")
def create_employee_api(
    name: str,
    email: str,
    dept_id: int,
    db: Session = Depends(get_db)
):
    return create_employee(db, name, email, dept_id)


@app.get("/employees")
def get_employees_api(db: Session = Depends(get_db)):
    return get_all_employees(db)



@app.get("/employees/{emp_id}")
def get_employee_api(emp_id: int, db: Session = Depends(get_db)):
    employee = get_employee(db, emp_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@app.put("/employees/{emp_id}")
def update_employee_api(
    emp_id: int,
    name: str,
    email: str,
    dept_id: int,
    db: Session = Depends(get_db)
):
    employee = update_employee(db, emp_id, name, email, dept_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@app.delete("/employees/{emp_id}")
def delete_employee_api(emp_id: int, db: Session = Depends(get_db)):
    employee = delete_employee(db, emp_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully"}