from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise # Allow us to register the models

# Create the app
app = FastAPI()

@app.get('/')
def index():
    return {"message": "Hello World"}

# Register the models with tortoise
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3", # The database url
    modules={"models": ["models"]}, # The models.py file
    generate_schemas=True, 
    add_exception_handlers=True,
)
