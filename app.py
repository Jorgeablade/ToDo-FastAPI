from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise # Allow us to register the models
from models import(task_pydantic, task_pydanticIn, task) # Import the models

# Jinja2 templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Create the app
app = FastAPI()

# Hello world
@app.get('/')
async def hello_world():
    return {"message": "Hello World"}

@app.post('/task')
# We create the function with sypplier_pydanticIn, because we are exliuding the id
async def add_task(task_info: task_pydanticIn):
    task_obj = await task.create(**task_info.dict(exclude_unset=True))
    # But in the response we want to know the id, so we use task_pydantic
    response = await task_pydantic.from_tortoise_orm(task_obj)
    return {"status": "success", "data": response}

# Get all tasks
@app.get('/task')
async def get_all_tasks():
    response = await task_pydantic.from_queryset(task.all())
    return {"status": "success", "data": response}

# Get a single task
@app.get('/task/{task_id}')
async def get_task(task_id: int, request: Request):
    response = await task_pydantic.from_queryset_single(task.get(id=task_id))
    return {"status": "success", "data": response}

# Update a task
@app.put('/task/{task_id}')
async def update_task(task_id: int, update_info: task_pydanticIn):
    await task.filter(id=task_id).update(**update_info.dict(exclude_unset=True))
    response = await task_pydantic.from_queryset_single(task.get(id=task_id))
    return {"status": "success", "data": response}

# Delete a task
@app.delete('/task/{task_id}')
async def delete_task(task_id: int):
    await task.filter(id=task_id).delete()
    return {"status": "success", "message": "task deleted"}

# Register the models with tortoise
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3", # The database url
    modules={"models": ["models"]}, # The models.py file
    generate_schemas=True, 
    add_exception_handlers=True,
)
