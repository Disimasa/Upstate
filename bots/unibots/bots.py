import json
import logging
import uvicorn
import asyncio
from pathlib import Path
from typing import List, Union
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import PlainTextResponse

from unibots.components import Card
from unibots.events import EventManager
from unibots.sessions import SessionManager
from unibots.connectors import RequestConnector, ResponseConnector, SDKConnector


class StarletteBot:
    def __init__(self, session_manager: SessionManager,
                 platforms_sdk: List[SDKConnector]):
        self.platforms_sdk = platforms_sdk
        self.session_manager = session_manager

        self.event_manager = EventManager()
        self.global_handlers = list()
        self.local_handlers = dict()

        __routes = [
            Route('/', endpoint=self.__server, methods=['POST']),
            Mount('/', StaticFiles(directory=Path(__file__).parent / 'hello_page', html=True))
        ]

        self.app = Starlette(routes=__routes)
        self.loop = asyncio.get_event_loop()
        self.app.add_event_handler(
            'startup', lambda: self.loop.create_task(self.session_manager.run_sessions_destroyer())
        )

    def run(self, host='127.0.0.1', port='8000'):
        uvicorn.run(self.app, host=host, port=port)

    def get_app(self):
        return self.app

    def add_local_handler(self, path, func, *args, **kwargs):
        self.local_handlers[path] = self.local_handlers.get(path, list()) + [(func, args, kwargs), ]

    def add_global_handler(self, func, *args, **kwargs):
        self.global_handlers.append((func, args, kwargs))

    def local_handler(self, func):
        def wrapper(*args, **kwargs):
            return self.add_local_handler(func, *args, **kwargs)
        return wrapper

    def upload_file(self, path: str) -> Card:
        ids = dict()
        for sdk in self.platforms_sdk:
            ids[f'{sdk.PLATFORM_NAME.lower()}_id'] = sdk.upload_file(path)
        return Card(path=path, **ids)

    # FIXME global_handler как декоратор не регистрирует хендлер!
    def global_handler(self, func, *args, **kwargs):
        # def wrapper(*args, **kwargs):
        self.add_global_handler(func, *args, **kwargs)
        # return wrapper

    def run_handlers(self, request: RequestConnector, response: ResponseConnector):
        session = self.session_manager.get_session(request.platform_id, create_new=True)

        if session.current_path not in self.local_handlers.keys():
            logging.warning(f'There is no such {session.current_path} path in local handlers')

        handlers = self.local_handlers.get(session.current_path, list()) + self.global_handlers
        for func, args, kwargs in handlers:
            result = func(request, response, session, *args, **kwargs)
            if result is not None:
                request, response = result
                break
        return request, response

    def get_sdk(self, request: dict) -> SDKConnector:
        for sdk in self.platforms_sdk:
            if sdk.is_platform_request(request):
                return sdk

    async def __server(self, request):
        request = json.loads(await request.body())
        self.event_manager.generate_event('new_request', request)
        sdk = self.get_sdk(request)
        if sdk is None:
            logging.warning('Got request from unknown platform, or you did not add specific SDK')
            return PlainTextResponse('ok')

        request = sdk.parse_request(request)
        response = sdk.create_response(request)

        request, response = self.run_handlers(request, response)
        return response.platform_based()
