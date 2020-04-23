import uvicorn
from fastapi import FastAPI
from models import User, Team
from tortoise import Tortoise


app = FastAPI(
    title='API for Upstate service',
    description='This is API for the service Upstate, '
                'which allows users to share their states between each other',
    version='0.0.1b',
    docs='/'
)


@app.on_event('startup')
async def startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas(safe=True)


@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()


@app.get('team/{token}')
def team_view(token: str):
    return {'Passed token': token}


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
