from tortoise import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    surname = fields.CharField(max_length=64)
    profession = fields.CharField(max_length=64)
    status = fields.CharField(default='Ещё не менял статус', max_length=32)
    token = fields.CharField(max_length=256)

    # tasks = fields.relational.ForeignKeyField('models.Task', null=True)
    # saved_statuses = fields.relational.ForeignKeyField('models.Status')

    def __str__(self):
        return f'Name: {self.name}, Surname: {self.surname}'


class Status(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=32)


class Task(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=128)
    completed = fields.BooleanField()


class Manager(User):
    id = fields.UUIDField(pk=True)
    is_manager = fields.BooleanField()


class Team(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=256)
    managers = fields.relational.ManyToManyField('models.User')
    members = fields.relational.ManyToManyField('models.Manager')
