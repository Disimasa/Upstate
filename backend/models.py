from tortoise import Model
from tortoise import fields


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    public_token = fields.CharField(max_length=256)
    private_token = fields.CharField(max_length=256)
    managers: fields.ManyToManyRelation['Manager'] = fields.ManyToManyField('models.Manager', related_name='teams')
    members: fields.ManyToManyRelation['User'] = fields.ManyToManyField('models.User', related_name='teams')


class Status(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=32)
    users = fields.relational.ManyToManyField('models.User', related_name='saved_statuses')

    def __str__(self):
        return f'Status: {self.title}'


class Task(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=128)
    completed = fields.BooleanField()
    # user = fields.Fo('models.User')


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    surname = fields.CharField(max_length=64)
    profession = fields.CharField(max_length=64)
    status = fields.CharField(default='Ещё не менял статус', max_length=32)
    private_token = fields.CharField(max_length=256)
    public_token = fields.CharField(max_length=256)

    web_id = fields.CharField(max_length=256, null=True)
    alice_id = fields.CharField(max_length=256, null=True)
    vk_id = fields.CharField(max_length=256, null=True)
    telegram_id = fields.CharField(max_length=256, null=True)

    teams: fields.ManyToManyRelation[Team]
    saved_statuses: fields.ManyToManyRelation[Status]

    def __str__(self):
        return f'Name: {self.name}, Surname: {self.surname}'


class Manager(User):
    id = fields.UUIDField(pk=True)

