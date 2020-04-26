import uvicorn
import logging
from starlette.config import Config

from unibots.components import Keyboard, Button, Gallery, Card
from unibots.sdk.alice import AliceSDK
from unibots.sdk.telegram import TelegramSDK
from unibots.sdk.vk import VKSDK
from unibots.bots import StarletteBot
from unibots.sessions import SessionManager, Session
from unibots.connectors import ResponseConnector, RequestConnector


def print_all_sessions(sessions):
    if len(sessions) > 0:
        logging.info('Destroying sessions:')
        for session in sessions:
            logging.info(session.global_store)


proxies = {
    # 'http': 'http://82.196.11.105:3128',
    'https': 'https://177.87.39.104:3128'
}

config = Config('.conf')
session_manager = SessionManager('/')
platforms_sdk = [
    TelegramSDK(config('TELEGRAM_TOKEN'), -452420031, proxies=proxies),
    VKSDK(config('VK_TOKEN')),
    AliceSDK(config('ALICE_TOKEN'), config('ALICE_AUTH'))
]
bot = StarletteBot(session_manager, platforms_sdk)
photo = None
app = bot.get_app()


@bot.local_handler
def local_handler(request: RequestConnector, response: ResponseConnector, session: Session):
    pass


@bot.global_handler
def handler_test(request: RequestConnector, response: ResponseConnector, session: Session):
    keyboard = Keyboard([
        [Button('Тестовая 1', color='primary')],
        [Button('Тестовая 2', color='positive'), Button('Тестовая 3', color='negative')],
    ], hide=False, inline=False)
    response.set_keyboard(keyboard)
    response.set_message(request.user_message)

    # Тестируем просто id - работает
    # response.set_media(photo)

    # Тестируем карточку - работает
    # response.set_media(Card(vk_id=photo, title='Замок', description='Это очень старый замок на горе'))
    # response.set_media(Card(path=photo, title='Замок', description='Это очень старый замок на горе'))

    # Тестируем группу id - работает
    # response.set_media(photo, photo, photo)

    # Тестируем группу карточек, с отправкой в виле галереи - работает
    # card1 = Card(vk_id=photo, title='Замок', description='Это очень старый замок на горе')
    # card2 = Card(vk_id=photo, title='Замок', description='Он находится в Европе')

    # card1 = Card(path=photo, title='Замок', description='Это очень старый замок на горе')
    # card2 = Card(path=photo, title='Замок', description='Он находится в Европе')
    # response.set_media(card1, card2)

    # Тестируем галерею - работает
    # gallery = Gallery(cards=[card1, card2], header='Картинки с замками', split=False)
    # gallery = Gallery(cards=[card1, card2], header='Картинки с замками', split=True)
    # gallery = Gallery(cards=[photo, photo], header='Картинки с замками', split=True)
    # gallery = Gallery(cards=[photo, photo], header='Картинки с замками', split=False)
    # response.set_media(gallery)
    return request, response


@app.on_event('startup')
def start():
    pass
    # global photo
    # photo = bot.upload_file('files/test2.jpg')


if __name__ == '__main__':
    uvicorn.run('bot_testing:app', reload=True, use_colors=True)
    # bot.run()
