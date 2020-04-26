import uvicorn
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import User, Team, Status, Manager
from api_models import UserToCreate, TeamToCreate, User_pydantic, \
     Team_pydantic, UserToJoin, UserToEdit, Public_User_pydantic,\
     Public_Team_pydantic, Manager_pydantic, ShowPublicTeam, ShowPrivateUser,\
     Status_pydantic

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


@app.get('/show/user', description='Shows User view', response_model=Public_User_pydantic)
async def user_view(public_token: str = Query(..., description='Public token of User')):
    user = await User.get_or_none(public_token=public_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return await Public_User_pydantic.from_tortoise_orm(user)


# TODO /show/team/private
@app.get('/show/team', response_model=ShowPublicTeam)
async def team_view(public_token: str = Query(..., description='Public token of team')):
    team = await Team.get_or_none(public_token=public_token)
    if team is None:
        raise HTTPException(status_code=404, detail='Team not found')
    return {
        'team': await Public_Team_pydantic.from_tortoise_orm(team),
        'members': [await Public_User_pydantic.from_tortoise_orm(user) for user in await team.members.all()]
    }


@app.post('/show/user/private', description='Shows private User view', response_model=ShowPrivateUser)
async def user_view(private_token: str = Body(..., description='Private token of User')):
    user = await User.get_or_none(private_token=private_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {
        'user': await User_pydantic.from_tortoise_orm(user),
        'saved_statuses': [await Status_pydantic.from_tortoise_orm(status)
                           for status in await user.saved_statuses.all()]
    }


@app.post('/create/user', description='Creates user if it was not in DB. Returns full User with private_token',
          response_model=ShowPrivateUser)
async def create_user(user_data: UserToCreate):
    user = await User.create(**tools.generate_user(user_data, data_for_persons_generator))
    for status in await Status.all().limit(len(fill_db.INITIAL_STATUSES)):
        await user.saved_statuses.add(status)

    return {
        'user': await User_pydantic.from_tortoise_orm(user),
        'saved_statuses': [await Status_pydantic.from_tortoise_orm(status)
                           for status in await user.saved_statuses.all()]
    }


@app.post('/create/team', description='Creates team binded to User. Accepts only private token',
          response_model=Team_pydantic)
async def create_team(team_data: TeamToCreate):
    user_token = team_data.creator_token
    user = await User.get_or_none(private_token=user_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    manager = await Manager.get_or_create(defaults=tools.generate_user(user, data_for_persons_generator))
    manager = manager[0]
    team = await Team.create(**tools.generate_team(manager))
    await team.managers.add(manager)
    return await Team_pydantic.from_tortoise_orm(team)


@app.post('/edit/user', description='Edit User info', response_model=ShowPrivateUser)
async def edit_user(user_data: UserToEdit):
    user = await User.get_or_none(private_token=user_data.private_token)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    update_data = dict()
    if user_data.new_name is not None:
        update_data['name'] = user_data.new_name
    if user_data.new_surname is not None:
        update_data['surname'] = user_data.new_surname
    if user_data.new_profession is not None:
        update_data['profession'] = user_data.new_profession
    if user_data.new_status is not None:
        update_data['status'] = user_data.new_status

    await user.update_from_dict(update_data)
    if user_data.new_saved_statuses is not None:
        statuses = await user.saved_statuses.all()
        if len(statuses) > 0:
            await user.saved_statuses.remove(*statuses)

        print(user_data.new_saved_statuses)
        for status_title in user_data.new_saved_statuses:
            new_status = await Status.get_or_none(title=status_title)
            if new_status is None:
                new_status = await Status.create(title=status_title)
            await user.saved_statuses.add(new_status)

    return {
        'user': await User_pydantic.from_tortoise_orm(user),
        'saved_statuses': [await Status_pydantic.from_tortoise_orm(status)
                           for status in await user.saved_statuses.all()]
    }


@app.post('/enter/team',
          description='Universal method for adding Users. Pass private User token and public Team token '
                      'to join as member, or private User token and private Team token to join as manager',
          response_model=ShowPublicTeam)
async def join_team(data: UserToJoin = Body(...)):
    if data.team_token.split(':')[0] == 'private':
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
    return {
        'team': await Public_Team_pydantic.from_tortoise_orm(team),
        'members': [await Public_User_pydantic.from_tortoise_orm(user) for user in await team.members.all()]
    }


@app.post('/admin/show')
async def admin_view():
    return {
        'Users': [await User_pydantic.from_tortoise_orm(user) for user in await User.all()],
        'Teams': [{
            'team': await Team_pydantic.from_tortoise_orm(team),
            'members': [await User_pydantic.from_tortoise_orm(member) for member in await team.members.all()],
            'managers': [await Manager_pydantic.from_tortoise_orm(manager) for manager in await team.managers.all()]
        } for team in await Team.all()]
    }


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
