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


# Let's try JWT tokens
import jwt
from passlib.hash import bcrypt

# Local imports
from config import DEFAULT_SETTINGS, TOKEN_URL
 
templates = Jinja2Templates(directory="templates")

SECRET_KEY = DEFAULT_SETTINGS.secret
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
     
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

    return {'access_token' : token, 'token_type' : 'bearer'}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)

@app.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user
        
############################################################################################################
############################################# DONT TOUCH ###################################################
############################################################################################################
@app.post('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

'''@app.get("/")
def home(request: Request):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "todo_list": todos})'''
 
@app.post("/create")
async def create_todo(request: Request, title: str):
    todo = await Todo.create(title=title, complete=False)
    return todo
 
 
@app.get("/update/{todo_id}")
async def update_todo(request: Request, todo_id: int):
    todo = await Todo.filter(id=todo_id).first()
    if not todo:
        return {"detail": "Todo item not found"}
    todo.complete = not todo.complete
    await todo.save()
 
@app.get("/delete/{todo_id}")
async def delete(request: Request, todo_id: int):
    todo = await Todo.filter(id=todo_id).first()
    await todo.delete()


register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app']},
    generate_schemas=True,
    add_exception_handlers=True
)