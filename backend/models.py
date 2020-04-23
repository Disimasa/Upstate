from tortoise import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    second_name = fields.CharField(max_length=64, default='')
    is_manager = fields.BooleanField(default=False)
    token = fields.CharField(max_length=256)


class Team(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=256)
