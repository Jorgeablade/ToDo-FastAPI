# Description: This is the main file of the project. It contains the FastAPI app and the routes. Idk how to to do routes in a separate file, so I just put them here.
from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

# Jinja2 imports
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.requests import Request
 
# Database imports
from tortoise.contrib.fastapi import register_tortoise

# Models imports
from models.user import User_Pydantic, UserIn_Pydantic
from db.models import User, Todo

# exceptions import
from exceptions import *

# Login system imports
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.responses import HTMLResponse

# Let's try JWT tokens
import jwt
from passlib.hash import bcrypt

import uvicorn

# Local imports
from config import DEFAULT_SETTINGS, TOKEN_URL
 
templates = Jinja2Templates(directory="/todo-list/todo/templates")

SECRET_KEY = DEFAULT_SETTINGS.secret
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

app = FastAPI()

# Get the id of the current user, so we can use it in the Todo model

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    # return await User_Pydantic.from_tortoise_orm(user)
    return user

     
async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise InvalidUserPass

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), SECRET_KEY)

    return {'access_token' : token, 'token_type': 'bearer'}

@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user
        
@app.get('/')
async def index(request: Request):
    # todos = await Todo.all()
    response = templates.TemplateResponse("login.html", {"request": request})
    # return RedirectResponse(url="/login", status_code=303)
    return response
        
@app.post('/login')
async def generate_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        # raise InvalidUserPass
        return RedirectResponse(url="/login", status_code=303)

    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), SECRET_KEY)
    response = templates.TemplateResponse("home.html", {"request": request})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@app.get('/home')
async def login(request: Request):
    todos = await Todo.all()
    return templates.TemplateResponse("home.html", {"request": request, "todo_list": todos})
                                      
# An admin endpoint just to see all the contents Todo table
@app.get("/database/todos")
async def get_all_todos_db(request: Request):
    todo = await Todo.all()
    return todo

# An admin endpoint just to see all the contents User table
@app.get("/database/users")
async def get_all_users_db(request: Request):
    user = await User.all()
    return user

@app.post("/create")
async def add(request: Request, title: str = Form(...)):
    todo = Todo(title=title)
    await todo.save()
    # todo_list = await Todo.all()
    # return templates.TemplateResponse("home.html", {"request": request, "todo_list": todo_list})
    return RedirectResponse(url="/home", status_code=303)
    
 
@app.get("/update/{todo_id}")
async def update_todo(request: Request, todo_id: int):
    todo = await Todo.filter(id=todo_id).first()
    if not todo:
        return {"detail": "Todo item not found"}
    todo.complete = not todo.complete
    await todo.save()
    return RedirectResponse(url="/home", status_code=303)
 
@app.get("/delete/{todo_id}")
async def delete(request: Request, todo_id: int):
    todo = await Todo.filter(id=todo_id).first()
    if not todo:
        return {"detail": "Todo item not found"}
    await todo.delete()
    
    return RedirectResponse(url="/home", status_code=303)

register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app']},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")