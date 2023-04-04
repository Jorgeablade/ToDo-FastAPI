from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class task(Model):
    id = fields.IntField(pk=True)
    task_title  = fields.CharField(max_length=100, nullable=False)
    task_description = fields.CharField(max_length=200, nullable=False)
    importance = fields.IntField(default=0, max_chars=10)
    date_of_creation = fields.DatetimeField(auto_now_add=True)

# create pydantic models

# create a pydantic model from the task model with all the fields
task_pydantic = pydantic_model_creator(task, name="task")

# create a pydantic model from the task model with all the fields except the id, this is used for creating a new task
# thats why we exclude the readonly fields, so that the id is not included
task_pydanticIn = pydantic_model_creator(task, name="taskIn", exclude_readonly=True)
