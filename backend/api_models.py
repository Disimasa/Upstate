from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field

from models import Team, User


class TeamToCreate(BaseModel):
    creator_token: str = Field(..., description='Token of user, who creates the team', example='fh14kl1km!6b')


class UserToCreate(BaseModel):
    platform_token: str = Field(..., description='Token or id of platform', example='fh14kl1km!6b')
    name: str = Field(None, description='Name of user from Telegram/VK', example='Ivan')
    surname: str = Field(None, description='Surname of user from Telegram/VK', example='Ivanov')


User_pydantic = pydantic_model_creator(User, name='User')
Team_pydantic = pydantic_model_creator(Team, name='Team')
