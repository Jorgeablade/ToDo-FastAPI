# Description: This is the main file of the project. It contains the FastAPI app and the routes. Idk how to to do routes in a separate file, so I just put them here.
from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

# Jinja2 imports
from starlette.templating import Jinja2Templates
 
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
        
        


'''# Verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)'''

# Get a hashed password
'''def get_password_hash(password):
    return pwd_context.hash(password)

# Get the user by the password
def get_user(db: Session, username: str):
    if username in db:
        return True
    else:
        return False

# authenticate the user
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Get the current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = InvalidUserPass
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Get the current active user
async def get_current_active_user(current_user: Annotated[models.User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Register a new user
@app.post("/users/", response_model=User)
async def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# login for access token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise InvalidUserPass
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get the current user
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return current_user

# Test read own items
@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]'''

'''@manager.user_loader()
def load_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user'''

        
'''@app.post("/auth/register")
def register(data: User, db: Session = Depends(get_db)):
    encoded_password = hashlib.sha256(data.password.encode()).hexdigest()
    new_user = models.User(username=data.username, password=encoded_password)
    user_in_db = load_user(data.username, db)
    if user_in_db:
        raise UsernameAlreadyTaken
    else:
        db.add(new_user)
        db.commit()
        return {"message": "User created successfully"}
    
@app.post("/auth/token")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_input = data.username
    password_hash = hashlib.sha256(data.password.encode('utf-8')).hexdigest()

    user_in_db = load_user(data.username, db)
    if not user_in_db:
        raise InvalidUserPass
        
    elif password_hash != user_in_db.password:
        raise InvalidUserPass

    access_token = manager.create_access_token(
        data=dict(sub=user_input)
    )
    return Token(access_token=access_token, token_type="bearer")'''




'''############################################################################################################
############################################# DONT TOUCH ###################################################
############################################################################################################
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
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    if todo.id != User.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this todo")
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

'''
register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['app']},
    generate_schemas=True,
    add_exception_handlers=True
)