import uvicorn
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import User, Team, Status, Manager
from api_models import UserToCreate, TeamToCreate, User_pydantic, \
    Team_pydantic, UserToJoin, Public_User_pydantic, Public_Team_pydantic
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


@app.get('/show/user', description='Shows User view')
async def user_view(public_token: str = Query(..., description='Public token of User')):
    user = await User.get_or_none(public_token=public_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return await Public_User_pydantic.from_tortoise_orm(user)


@app.get('/show/team')
async def team_view(public_token: str = Query(..., description='Public token of team')):
    team = await Team.get_or_none(public_token=public_token)
    if team is None:
        raise HTTPException(status_code=404, detail='Team not found')
    return await Public_Team_pydantic.from_tortoise_orm(team)


@app.post('/create/user', description='Creates user if it was not in DB. Returns full User with private_token')
async def create_user(user_data: UserToCreate):
    user = await User.get_or_create(defaults=tools.generate_user(user_data))
    user = user[0]  # get_or_create returns tuple
    return await User_pydantic.from_tortoise_orm(user)


@app.post('/create/team', description='Creates team binded to User. Accepts only private token')
async def create_team(team_data: TeamToCreate):
    user_token = team_data.creator_token
    user = await User.get_or_none(private_token=user_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    manager = await Manager.get_or_create(defaults=tools.generate_user(user_token))
    manager = manager[0]
    team = await Team.create(**tools.generate_team(manager))
    return await Team_pydantic.from_tortoise_orm(team)


@app.post('/enter/team',
          description='Universal method for adding Users. Pass private User token and public Team token '
                      'to join as member, or private User token and private Team token to join as manager')
async def join_team(is_manager: bool = False, data: UserToJoin = Body(...)):
    if is_manager:
        manager = await Manager.get_or_none(private_token=data.user_token)
        team = await Team.get_or_none(private_token=data.team_token)
        if manager is None or team is None:
            raise HTTPException(status_code=404, detail='Access denied')
        await team.managers.add(manager)

    else:
        user = await User.get_or_none(private_token=data.user_token)
        team = await Team.get_or_none(public_token=data.team_token)
        if user is None or team is None:
            raise HTTPException(status_code=404, detail='User or team not found')
        await team.members.add(user)


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
