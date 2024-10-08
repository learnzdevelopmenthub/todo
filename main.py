# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models, schemas, crud, auth, database
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Learnz Development Hub's Todo API"}


@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos", response_model=list[schemas.Todo])
def read_todos(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return crud.get_todos_for_user(db, user_id=user_id)

@app.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return crud.create_todo_for_user(db, todo, user_id=user_id)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    success = crud.delete_todo_for_user(db, todo_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

@app.put("/todos/{todo_id}/complete")
def update_todo_completion(todo_id: int, completed: bool, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = auth.decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    updated_todo = crud.update_todo_completion(db, todo_id, user_id, completed)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

# Add this block after creating the FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
