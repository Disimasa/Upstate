import httpx
import uvicorn
import logging

from starlette.config import Config
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.applications import Starlette

from unibots.sdk.telegram import TelegramRequest, TelegramResponse, TelegramSDK
from unibots.components import Keyboard, Button, Card, Gallery

sdk, token, photo = None, None, None


async def main(request):
    request: TelegramRequest = TelegramRequest(await request.body())
    response: TelegramResponse = sdk.create_response(request)

    keyboard = Keyboard(
        buttons=[[
            Button(text='Hello', callback='2'),
            Button(text='Word', callback='Word')
        ]], inline=True, hide=True)
    response.set_keyboard(keyboard)
    response.set_message(request.user_message)

    # Тестируем просто id - работает
    response.set_media(photo)

    # Тестируем карточку - работает
    # response.set_media(Card(path=photo, title='Замок', description='Это очень старый замок на горе'))
    # response.set_media(Card(telegram_id=photo, title='Замок', description='Это очень старый замок на горе'))

    # Тестируем группу id - работает
    # response.set_media(photo, photo, photo)

    card1 = Card(telegram_id=photo, title='Замок', description='Это очень старый замок на горе')
    card2 = Card(telegram_id=photo, title='Замок', description='Он находится в Европе')

    # card1 = Card(path=photo, title='Замок', description='Это очень старый замок на горе')
    # card2 = Card(path=photo, title='Замок', description='Он находится в Европе')

    # Тестируем группу карточек, с отправкой в виле галереи - работает
    # response.set_media(card1, card2, card1)

    # Тестируем галерею - работает
    # gallery = Gallery(cards=[card1, card2, card1], header='Картинки с замками', split=False)
    gallery = Gallery(cards=[card1, card2, card1], header='Картинки с замками', split=True)
    response.set_media(gallery)

    return response.platform_based()


routes = [
    Route('/', main, methods=['POST'])
]

app = Starlette(routes=routes)

server_url = 'https://06be1d22.ngrok.io/'
proxies = {
    # 'http': 'http://82.196.11.105:3128',
    'https': 'https://177.87.39.104:3128'
}


@app.on_event('startup')
def start():
    global token, sdk, photo
    config = Config('.conf')
    token = config('TELEGRAM_TOKEN')
    sdk = TelegramSDK(token, -452420031, proxies=proxies)

    with httpx.Client(proxies=proxies) as client:
        url = f'{sdk.BASE_URL}{sdk.token}/setWebhook'
        res = client.get(url, params={'url': server_url, 'max_connections': 1})
        logging.info(res.text)

    photo = sdk.upload_file('files/test.jpg')
    # photo = 'https://s1.1zoom.ru/big3/145/Neuschwanstein_Autumn_Germany_Castles_Bavaria_Crag_558659_5185x3457.jpg'
    # photo = 'files/test.jpg'


if __name__ == '__main__':
    uvicorn.run('telegram_testing:app', reload=True, use_colors=True)
