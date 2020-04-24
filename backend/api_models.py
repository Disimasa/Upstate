from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field

from models import Team, User


class TeamToCreate(BaseModel):
    creator_token: str = Field(..., description='Private token of user, who creates the team', example='fh14kl1km!6b')


class UserToJoin(BaseModel):
    team_token: str = Field(..., description='The public token of team', example='fh14kl1km!6b')
    user_token: str = Field(..., description='The private token of user', example='fh14kl1km!6b')


class UserToCreate(BaseModel):
    platform_token: str = Field(..., description='Token or id of platform', example='fh14kl1km!6b')
    name: str = Field(None, description='Name of user from Telegram/VK', example='Ivan')
    surname: str = Field(None, description='Surname of user from Telegram/VK', example='Ivanov')


User_pydantic = pydantic_model_creator(User, name='User')
Team_pydantic = pydantic_model_creator(Team, name='Team')
Public_User_pydantic = pydantic_model_creator(User, name='User', exclude=('private_token',))
Public_Team_pydantic = pydantic_model_creator(Team, name='Team', exclude=('managers_token', 'managers'))
