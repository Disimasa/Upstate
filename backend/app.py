import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from models import User, Team, Status, Manager
from api_models import UserToCreate, TeamToCreate, User_pydantic, Team_pydantic
from tortoise import Tortoise
import tools

INITIAL_STATUSES = ['Чилю', 'Ботаю', 'Играю']

app = FastAPI(
    title='Upstate API',
    description='This is API for the service Upstate, '
                'which allows users to share their states between each other',
    version='0.0.1b',
    docs_url='/'
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas(safe=True)
    for status in INITIAL_STATUSES:
        if Status.get_or_none(status=status) is None:
            await Status.create(status=status)


@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()


@app.get('/team/{token}')
async def team_view(token: str):
    return {'Passed token': token}


@app.post('/create/user')
async def create_user(user_data: UserToCreate):
    user = await User.get_or_create(defaults=tools.generate_user(user_data))
    user = user[0]  # get_or_create returns tuple
    return await User_pydantic.from_tortoise_orm(user)


@app.post('/create/team')
async def create_team(team_data: TeamToCreate):
    user_token = team_data.creator_token
    user = await User.get_or_create(defaults=tools.generate_user(user_token))
    manager = await Manager.get_or_create(defaults=tools.generate_user(user_token))
    manager = manager[0]
    team = await Team.create(**tools.generate_team(manager))
    return await Team_pydantic.from_tortoise_orm(team)

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
