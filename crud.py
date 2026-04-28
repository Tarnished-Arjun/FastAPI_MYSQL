from sqlalchemy.orm import Session
from models import Item, Employee


def create_item(db: Session, name: str, description: str, price: int):
    item = Item(name=name, description=description, price=price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_employee(db: Session, name: str, email: str, dept_id: int):
    employee = Employee(name=name, email=email, dept_id=dept_id)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_all_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, emp_id: int):
    return db.query(Employee).filter(Employee.id == emp_id).first()


def update_employee(db: Session, emp_id: int, name: str, email: str, dept_id: int):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()

    if employee:
        employee.name = name
        employee.email = email
        employee.dept_id = dept_id
        db.commit()
        db.refresh(employee)

    return employee


def delete_employee(db: Session, emp_id: int):
    employee = db.query(Employee).filter(Employee.id == emp_id).first()

    if employee:
        db.delete(employee)
        db.commit()

    return employee