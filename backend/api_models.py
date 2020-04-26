from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field
from typing import List, Union
from models import Team, User, Manager, Status, Task
from enum import Enum


class Platforms(Enum):
    alice = 'alice'
    vk = 'vk'
    telegram = 'telegram'
    web = 'web'


class TeamToCreate(BaseModel):
    creator_token: str = Field(..., description='Private token of user, who creates the team',
                               example='fh14kl1km!6b', max_length=256)


class UserToJoin(BaseModel):
    team_token: str = Field(..., description='The public token of team',
                            example='fh14kl1km!6b', max_length=256)
    user_token: str = Field(..., description='The private token of user',
                            example='fh14kl1km!6b', max_length=256)


class TaskToGet(BaseModel):
    completed: bool
    description: str


class UserToEdit(BaseModel):
    private_token: str = Field(..., description='Private token of User', max_length=256)
    new_name: str = Field(None, description='Set a new name if it was changed', max_length=64)
    new_surname: str = Field(None, description='Set a new surname if it was changed', max_length=64)
    new_profession: str = Field(None, description='Set a new profession if it was changed', max_length=64)
    new_status: str = Field(None, description='Set a new status if it was changed', max_length=32)
    new_saved_statuses: List[str] = Field(None, description='Set new list with titles of statuses')
    new_tasks: List[TaskToGet] = Field(None, description='Set a new list of tasks')


class UserToCreate(BaseModel):
    platform_id: str = Field(..., description='Token or id of platform', example='fh14kl1km!6b', max_length=256)
    platform_name: Platforms = Field(..., description='Platform name allowed: alice/vk/telegram/web', example='web')
    name: str = Field(None, description='Name of user from Telegram/VK', example='Ivan', max_length=64)
    surname: str = Field(None, description='Surname of user from Telegram/VK', example='Ivanov', max_length=64)


Status_pydantic = pydantic_model_creator(Status, name='Status')
User_pydantic = pydantic_model_creator(User, name='UserPrivate')
Manager_pydantic = pydantic_model_creator(Manager, name='UserPrivate')
Team_pydantic = pydantic_model_creator(Team, name='TeamPrivate', exclude=('private_token', ))
Public_User_pydantic = pydantic_model_creator(User, name='UserPublic',
                                              exclude=('private_token', 'vk_id', 'alice_id', 'telegram_id', 'web_id'))
Public_Team_pydantic = pydantic_model_creator(Team, name='TeamPublic',
                                              exclude=('managers_token', 'managers', 'private_token'))
Task_pydantic = pydantic_model_creator(Task, name='Task')


class ShowPublicTeam(BaseModel):
    members: List[Public_User_pydantic]
    team: Public_Team_pydantic


class ShowPublicUser(BaseModel):
    user: Public_User_pydantic
    tasks: List[Task_pydantic]


class ShowPrivateUser(BaseModel):
    user: User_pydantic
    saved_statuses: List[Status_pydantic]
    tasks: List[Task_pydantic]
