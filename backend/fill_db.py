from models import Status, User, Team


INITIAL_STATUSES = ['Чилю', 'Ботаю', 'Играю']


async def statuses():
    for status in INITIAL_STATUSES:
        if Status.get_or_none(status=status) is None:
            await Status.create(status=status)
