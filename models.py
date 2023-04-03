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

# create a pydantic model from the Product model with all the fields
product_pydantic = pydantic_model_creator(Product, name="Product")

# create a pydantic model from the Product model with all the fields except the id, this is used for creating a new product
# thats why we exclude the readonly fields, so that the id is not included
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

# create a pydantic model from the Supplier model with all the fields
supplier_pydantic = pydantic_model_creator(Supplier, name="Supplier")

# create a pydantic model from the Supplier model with all the fields except the id, this is used for creating a new supplier
# thats why we exclude the readonly fields, so that the id is not included
supplier_pydanticIn = pydantic_model_creator(Supplier, name="SupplierIn", exclude_readonly=True)
