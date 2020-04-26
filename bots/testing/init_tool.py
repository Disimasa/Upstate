import httpx
import json
import logging
import uvicorn
from typing import Callable
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.config import Config
from starlette.routing import Route

from unibots.sdk.telegram import TelegramSDK

SERVER_URL = 'https://c65a708e.ngrok.io/'
PROXIES = {
    # 'http': 'http://82.196.11.105:3128',
    'https': 'https://177.87.39.104:3128'
}

vk_confirmation = None


async def server_starting():
    global vk_confirmation
    config = Config('.conf')
    token = config('TELEGRAM_TOKEN')
    vk_confirmation = config('VK_CONFIRMATION')

    with httpx.Client(proxies=PROXIES) as client:
        url = f'https://api.telegram.org/bot{token}/setWebhook'
        res = client.get(url, params={'url': SERVER_URL, 'max_connections': 1})
        logging.info(res.text)


async def server(request):
    request = json.loads(await request.body())
    if request.get('type', None) == 'confirmation':
        return PlainTextResponse(vk_confirmation)


routes = [
    Route('/', server, methods=['POST'])
]

app = Starlette(routes=routes, on_startup=[server_starting])

if __name__ == '__main__':
    uvicorn.run('init_tool:app', reload=True, use_colors=True)
