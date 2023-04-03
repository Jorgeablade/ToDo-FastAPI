from fastapi import FastAPI

# Create the app
app = FastAPI()

@app.get('/')
def index():
    return {"message": "Hello World2"}