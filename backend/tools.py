from models import User, Manager
from api_models import UserToCreate
import pandas as pd
from hashlib import sha256
from typing import List
import datetime


def generate_tokens_onetime(data: List[str]):
    data = ':'.join(data)
    data += datetime.datetime.now().strftime('%d%B%Y')
    private, public = bytes(data + 'gWekqpoie12', encoding='utf8'), bytes(data, encoding='utf8')
    return 'private:'+sha256(private).hexdigest(), 'public:'+sha256(public).hexdigest()


def generate_user(user_data: UserToCreate, gen_data: pd.DataFrame):
    random_person = gen_data.sample(1)
    random_person = random_person.iloc[0]
    if user_data.name == '' and user_data.surname == '' or \
            user_data.name is None and user_data.surname is None:
        name = random_person['name']
        surname = random_person['surname']
        profession = random_person['profession']
    else:
        name = user_data.name
        surname = user_data.surname
        profession = ''
    private_token, public_token = generate_tokens_onetime([profession, name, surname])
    return {'name': name, 'surname': surname, 'profession': profession,
            f'{user_data.platform_name.value}_id': user_data.platform_id,
            'private_token': private_token, 'public_token': public_token}


def generate_team(manger):
    private_token, public_token = generate_tokens_onetime([manger.name, manger.surname])
    return {'public_token': public_token, 'private_token': private_token, 'name': 'Какая-то команда'}
