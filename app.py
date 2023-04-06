from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
 
from sqlalchemy.orm import Session

# Trying ot make a login system
from fastapi_login import LoginManager
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseSettings, BaseModel, UUID4
from fastapi_login.exceptions import InvalidCredentialsException

import models
from database import SessionLocal, engine
 
models.Base.metadata.create_all(bind=engine)


class Settings(BaseSettings):
    secret: str  # automatically taken from environment variable


class UserCreate(BaseModel):
    username: str
    password: str


class User(UserCreate):
    id: UUID4

DEFAULT_SETTINGS = Settings(_env_file=".env")
DB = {
    "users": {}
}

TOKEN_URL = "/auth/token"
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI()

manager = LoginManager(DEFAULT_SETTINGS.secret, TOKEN_URL)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@manager.user_loader()
def load_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.username == username).first()
    return user
 
# Add user to database, just to test
@app.post("/auth/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    new_user = models.user(username=data.username, password=data.password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# Now we have to define a way to let the user login in our app. Therefore we will create a new route:
@app.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_input = data.username
    password = data.password

    user_in_db = load_user(data.username, db)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect (username) or password1")
        
    elif password != user_in_db.password:
        raise HTTPException(status_code=400, detail="Incorrect username or (password)")

    access_token = manager.create_access_token(
        data=dict(sub=user_input)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "todo_list": todos})
 
@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
 
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
 
 
@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()
 
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
 
 
@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db), user=Depends(manager)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
