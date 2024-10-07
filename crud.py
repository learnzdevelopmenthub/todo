# crud.py
from sqlalchemy.orm import Session
import models
import schemas
import auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and auth.verify_password(password, user.hashed_password):
        return user
    return False

def create_todo_for_user(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos_for_user(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def delete_todo_for_user(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False

def update_todo_completion(db: Session, todo_id: int, user_id: int, completed: bool):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()
    if db_todo:
        db_todo.completed = completed
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None
