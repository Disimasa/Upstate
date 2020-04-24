from models import User, Manager


def generate_tokens(data: str):
    # if data['sketch'] == 'team':
    #     return '12414121519809@1'
    return '124142512', '51qwrq412'


def generate_user(data: str):
    private_token, public_token = generate_tokens(data)
    return {'name': 'Иван', 'surname': 'Иванов', 'profession': 'Developer',
            'private_token': private_token, 'public_token': public_token}


def generate_team(manger):
    data = manger.name + manger.surname
    private_token, public_token = generate_tokens(data)
    return {'manager_id': manger.pk, 'public_token': public_token,
            'private_token': private_token, 'name': 'Какая-то команда'}
