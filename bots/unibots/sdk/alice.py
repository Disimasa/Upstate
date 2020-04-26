import json
import logging

import httpx
from typing import Any, List, Dict
from os.path import getsize
from starlette.responses import JSONResponse

from unibots.components import Keyboard, Card, Gallery
from unibots.sdk.abstract import AbstractResponse, AbstractRequest, AbstractSDK
from unibots.tools import cut_text, is_url, auto_type


class AliceResponse(AbstractResponse):
    def __init__(self, sdk, session, version="1.0", message_default: str = 'Навык запущен'):
        super(AliceResponse, self).__init__(sdk)

        self.params: Any = {
            'response': {
                'text': message_default,
                'end_session': False,
            },
            'session': session,
            'version': version
        }

    # TODO: Удалить метод, придумать интеграцию через SessionManager
    def end(self):
        self.params['response']['end_session'] = True

    def set_message(self, text: str):
        text = cut_text(text, 1024, 'Message length must be less then 1024. Message text will be cut!')
        self.params['response']['text'] = text

    def __path_upload_card(self, card):
        if (card.alice_id is None) and (card.path is not None):
            card.alice_id = self.sdk.upload_file(card.path)
        elif (card.alice_id is None) and (card.path is None):
            logging.warning(f'The card does not have path or alice_id: {card}')
            return

    # def __card_conflict_resolver(self):
    def set_media(self, *content: Card or Gallery or str):
        content = self.parse_media_args(content)
        if isinstance(content, Card):
            self.__path_upload_card(content)
            content = content.alice_card
        elif isinstance(content, Gallery):
            for card in content.cards:
                self.__path_upload_card(card)
            content = content.alice_gallery
        self.params['response']['card'] = content

    def set_keyboard(self, keyboard: Keyboard):
        self.params['response']['buttons'] = keyboard.alice_keyboard

    def platform_based(self) -> JSONResponse:
        return JSONResponse(self.params)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.params)


class AliceRequest(AbstractRequest):
    @property
    def user_message(self) -> str:
        # FIXME: API не возвращает текст, который появляется при нажатия на кнопку.
        # FIXME: Пока что используем Payload в компоненте Button
        if self.request['request']['type'] == 'ButtonPressed':
            return self.request['request']['payload']['text']
        return self.request['request']['command']

    @property
    def platform_id(self) -> str:  # FIXME user_id?
        return str(self.request['session']['session_id'])

    def user_id(self) -> int:
        pass

    @property
    def session(self):
        return self.request['session']

    @property
    def version(self):
        return self.request['version']


class AliceSDK(AbstractSDK):
    BASE_URL = 'https://dialogs.yandex.net/api/v1/skills/'
    PLATFORM_NAME = 'Alice'

    def __init__(self, token: str, auth_token: str):
        super(AliceSDK, self).__init__(token)
        self.auth_token = auth_token

    @staticmethod
    def is_platform_request(request: dict) -> bool:
        return request.get('request', False) and request.get('session', False)

    @staticmethod
    def parse_request(request: str or dict) -> AliceRequest:
        return AliceRequest(request)

    def create_response(self, request: AliceRequest) -> AliceResponse:
        return AliceResponse(self, request.session, request.version)

    def upload_file(self, path: str) -> str or None:
        if auto_type(path) == 'photo':
            if is_url(path):
                response = httpx.post(
                    f'{self.BASE_URL}/{self.token}/images',
                    headers={'Authorization': f'OAuth {self.auth_token}'},
                    json={'url': path}
                ).json()
            else:
                if 1. <= getsize(path) / 1024 <= 1024.:
                    response: Any = httpx.post(
                        f'{self.BASE_URL}/{self.token}/images',
                        headers={'Authorization': f'OAuth {self.auth_token}'},
                        files={'file': open(path, 'rb')}
                    ).json()
                else:
                    raise ValueError(f'Size of file must be between 1KB and 1MB! '
                                     f'Yours: {round(getsize(path)/1024, 2)}MB')
            logging.debug(response)
            _id = response['image']['id']

            self.cache_store[path] = _id
            return _id
        logging.warning('Yandex dialogs supports only images and sounds')
