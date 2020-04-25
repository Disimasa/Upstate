import uvicorn
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import User, Team, Status, Manager
from api_models import UserToCreate, TeamToCreate, User_pydantic, \
     Team_pydantic, UserToJoin, UserToEdit, Public_User_pydantic, Public_Team_pydantic
from tortoise import Tortoise
import tools
import fill_db
import pandas as pd


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

data_for_persons_generator = None


@app.on_event('startup')
async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas(safe=True)
    await fill_db.statuses()
    global data_for_persons_generator
    data_for_persons_generator = pd.read_csv('persons.csv').fillna('')


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
    return {
        'team': await Public_Team_pydantic.from_tortoise_orm(team),
        'members': [await Public_User_pydantic.from_tortoise_orm(user) for user in await team.members.all()]
    }


@app.post('/create/user', description='Creates user if it was not in DB. Returns full User with private_token')
async def create_user(user_data: UserToCreate):
    user = await User.create(**tools.generate_user(user_data, data_for_persons_generator))
    return await User_pydantic.from_tortoise_orm(user)


@app.post('/create/team', description='Creates team binded to User. Accepts only private token')
async def create_team(team_data: TeamToCreate):
    user_token = team_data.creator_token
    user = await User.get_or_none(private_token=user_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    manager = await Manager.get_or_create(defaults=tools.generate_user(user, data_for_persons_generator))
    manager = manager[0]
    team = await Team.create(**tools.generate_team(manager))
    return await Team_pydantic.from_tortoise_orm(team)


@app.post('/edit/user', description='Edit User info')
async def edit_user(user_data: UserToEdit):
    user = User.get_or_none(private_token=user_data.private_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if user_data.new_name is not None:
        user.name = user_data.new_name
    if user_data.new_surname is not None:
        user.surname = user_data.new_surname
    if user_data.new_profession is not None:
        user.profession = user_data.new_profession
    if user_data.new_status is not None:
        user.status = user_data.new_status
    if user_data.new_saved_statuses is not None:
        for status_title in user_data.new_saved_statuses:
            status = await Status.get_or_create(title=status_title)
            status.users.add(user)


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


@app.post('/admin/show')
async def admin_view():
    return {
        'Users': [await User_pydantic.from_tortoise_orm(user) for user in await User.all()],
        'Teams': [{
            'team': await Team_pydantic.from_tortoise_orm(team),
            'members': [await User_pydantic.from_tortoise_orm(member) for member in await team.members.all()],
            'managers': [await User_pydantic.from_tortoise_orm(manager) for manager in await team.managers.all()]
        } for team in await Team.all()]
    }

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
