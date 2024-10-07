from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True