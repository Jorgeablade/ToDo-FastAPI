from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise # Allow us to register the models
from models import(supplier_pydantic, supplier_pydanticIn, Supplier)

# Create the app
app = FastAPI()

@app.get('/')
def index():
    return {"message": "got to /docs or /redoc for the API documentation"}

@app.post('/supplier')
# We create the function with sypplier_pydanticIn, because we are exliuding the id
async def add_supplier(supplier_info: supplier_pydanticIn):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    # But in the response we want to know the id, so we use supplier_pydantic
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "success", "data": response}

# Get all suppliers
@app.get('/supplier')
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "success", "data": response}

# Get a single supplier
@app.get('/supplier/{supplier_id}')
async def get_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "success", "data": response}

# Update a supplier
@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    await Supplier.filter(id=supplier_id).update(**update_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "success", "data": response}

# Delete a supplier
@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id: int):
    await Supplier.filter(id=supplier_id).delete()
    return {"status": "success", "message": "supplier deleted"}

# Register the models with tortoise
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3", # The database url
    modules={"models": ["models"]}, # The models.py file
    generate_schemas=True, 
    add_exception_handlers=True,
)
