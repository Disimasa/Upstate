from tortoise import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    surname = fields.CharField(max_length=64)
    profession = fields.CharField(max_length=64)
    status = fields.CharField(default='Ещё не менял статус', max_length=32)
    private_token = fields.CharField(max_length=256)
    public_token = fields.CharField(max_length=256)

    def __str__(self):
        return f'Name: {self.name}, Surname: {self.surname}'


class Status(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=32)
    saved_statuses = fields.relational.ManyToManyField('models.User')


class Task(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=128)
    completed = fields.BooleanField()
    user = fields.relational.ForeignKeyField('models.User')


class Manager(User):
    id = fields.UUIDField(pk=True)


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    public_token = fields.CharField(max_length=256)
    private_token = fields.CharField(max_length=256)
    managers = fields.relational.ManyToManyField('models.User')
    members = fields.relational.ManyToManyField('models.Manager')
