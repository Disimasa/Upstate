from unibots.sdk.alice import AliceRequest, AliceResponse, AliceSDK
from starlette.routing import Route, Mount
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.config import Config
import uvicorn

from unibots.components import Button, Keyboard, Card, Gallery

sdk, photo = None, None


async def start():
    global sdk, photo
    config = Config('.conf')
    sdk = AliceSDK(token=config('ALICE_TOKEN', cast=str),
                   auth_token=config('ALICE_AUTH', cast=str))
    # photo = sdk.upload_file('files/test2.jpg')
    # photo = 'https://facte.ru/wp-content/uploads/2017/02/zamki-i-kreposti.jpg'
    # photo = 'files/test2.jpg'


async def testing(request):
    request: AliceRequest = sdk.parse_request(await request.body())
    response = sdk.create_response(request)

    keyboard = Keyboard([
        [Button('Тестовая 1', color='primary')],
        [Button('Тестовая 2', color='positive'), Button('Тестовая 3', color='negative')],
    ], hide=True, inline=False)
    response.set_keyboard(keyboard)
    response.set_message(request.user_message)

    # TODO async upload

    # Тестируем просто id - работает
    # response.set_media(photo)

    # Тестируем карточку - работает
    # response.set_media(Card(alice_id=photo, title='Замок', description='Это очень старый замок на горе'))
    # response.set_media(Card(path=photo, title='Замок', description='Это очень старый замок на горе'))

    # Тестируем группу id - работает
    # response.set_media(photo, photo)

    # card1 = Card(alice_id=photo, title='Замок', description='Это очень старый замок на горе')
    # card2 = Card(alice_id=photo, title='Замок', description='Он находится в Европе')

    # Тестируем группу карточек, с отправкой в виле галереи - работает
    # response.set_media(card1, card2)

    # Тестируем галерею - работает
    # gallery = Gallery(cards=[card1, card2], header='Картинки с замками', split=True)
    # gallery = Gallery(cards=[card1, card2], header='Картинки с замками', split=False)
    # response.set_media(gallery)

    return response.platform_based()


routes = [
    Route('/', testing, methods=['POST']),
    Mount('/', StaticFiles(directory='../unibots/hello_page', html=True))
]

app = Starlette(routes=routes, on_startup=[start])

if __name__ == '__main__':
    uvicorn.run('alice_testing:app', reload=True, use_colors=True)
