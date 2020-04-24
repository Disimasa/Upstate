import uvicorn
from fastapi import FastAPI, Body
from models import User, Team, Status
from api_models import UserToCreate, TeamToCreate
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
    token = tools.generate_token('13142141241')
    user = await User.get_or_none(token=token)
    if user is None:
        generated_data = tools.generate_person()
        await User.create(token=token, **generated_data,
                          # status='Еще не менял статус',
                          # saved_statuses_id=0
                          )
    return {'token': token}


@app.post('/create/team')
async def create_team(team_data: TeamToCreate):
    token = tools.generate_token('3124rqwqrw')


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
