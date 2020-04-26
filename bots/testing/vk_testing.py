import uvicorn
import logging

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.config import Config
from starlette.datastructures import Secret

from unibots.sdk.vk import VKRequest, VKResponse, VKSDK
from unibots.components import Keyboard, Button, Card, Gallery


sdk, photo, VK_TOKEN = None, None, None


async def starting():
    global sdk, photo, VK_TOKEN
    config = Config('.conf')
    VK_TOKEN = config('VK_TOKEN', cast=str)
    sdk = VKSDK(VK_TOKEN)

    # photo = sdk.upload_file('files/test.jpg')
    # photo = 'files/test.jpg'
    # photo = 'https://facte.ru/wp-content/uploads/2017/02/zamki-i-kreposti.jpg'


async def testing(request):
    request: VKRequest = sdk.parse_request(await request.body())
    if request.type == 'confirmation':
        return PlainTextResponse('a173a127')
    response = sdk.create_response(request)
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
    # response.set_media(gallery)

    return response.platform_based()


routes = [
    Route('/', testing, methods=['POST'])
]

app = Starlette(routes=routes, on_startup=[starting])


if __name__ == '__main__':
    uvicorn.run('vk_testing:app', reload=True, use_colors=True)
