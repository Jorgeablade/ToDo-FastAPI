from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Product(Model):
    id = fields.IntField(pk=True)
    name  = fields.CharField(max_length=30, nullable=False) # Can't be null
    quantity_in_stock = fields.IntField(default=0)
    quantity_sold = fields.IntField(default=0)
    unit_price = fields.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    supplied_by = fields.ForeignKeyField('models.Supplier', related_name='products')
    revenue = fields.DecimalField(max_digits=20, decimal_places=2, default=0.0)

class Supplier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40)
    company = fields.CharField(max_length=20)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=15)

# create pydantic models

# create pydantic models with all fields for admin
product_pydantic = pydantic_model_creator(Product, name="Product")

# create pydantic models with exclude fields for clients, so they can't change the id
product_in_pydantic = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

# create pydantic models with all fields for admin
supplier_pydantic = pydantic_model_creator(Supplier, name="Supplier")

# create pydantic models with exclude fields for clients, so they can't change the id
supplier_in_pydantic = pydantic_model_creator(Supplier, name="SupplierIn", exclude_readonly=True)
