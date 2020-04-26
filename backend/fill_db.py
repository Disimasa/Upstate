import logging
from models import Status, User, Team


INITIAL_STATUSES = ['Чилю', 'Ботаю', 'Играю']


async def statuses():
    for status in INITIAL_STATUSES:
        if await Status.get_or_none(title=status) is None:
            new_status = await Status.create(title=status)
            logging.info(f'Added new status: {new_status}')