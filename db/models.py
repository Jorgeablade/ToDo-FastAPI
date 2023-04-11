import datetime
from passlib.hash import bcrypt
from tortoise.models import Model
from tortoise import fields

class Todo(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(100)
    complete = fields.BooleanField(default=False)
    # DateTime now()
    # date = fields.DatetimeField(default=datetime.datetime.now)

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(100, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)