import io
import json
import logging
from copy import deepcopy
from random import randint
from typing import Any

import httpx
from starlette.responses import PlainTextResponse

from unibots.components import Keyboard, Card, Gallery
from unibots.sdk.abstract import AbstractResponse, AbstractRequest, AbstractSDK
from unibots.tools import auto_type, is_url


class VKResponse(AbstractResponse):
    def __init__(self, sdk, user_id, message_default: str = 'Бот запущен'):
        super(VKResponse, self).__init__(sdk)
        self.chat_id = user_id
        self.message_default = message_default
        self.params = {
            'user_id': self.chat_id,
            'message': self.message_default,
            # ВК работает как конская з.лупа
            'random_id': randint(0, 9223372036854775807),
            'keyboard': json.dumps({'buttons': [], 'one_time': True})
        }
        self.params.update(self.sdk.BASE_PARAMS)
        self.__query = list()

    def set_message(self, text: str):
        self.params['message'] = text

    def __path_upload_card(self, card):
        if card.vk_id is None and card.path is not None:
            card.vk_id = self.sdk.upload_file(card.path)
        elif (card.vk_id is None) and (card.path is None):
            logging.warning(f'The card does not have path or vk_id: {card}')
            return

    def set_media(self, *content: Card or Gallery or str):
        self.__query = list()
        content = self.parse_media_args(content)

        if isinstance(content, Card):
            self.__path_upload_card(content)
            self.params.update(content.vk_card)

        elif isinstance(content, Gallery):
            for card in content.cards:
                self.__path_upload_card(card)

            for card in content.vk_gallery:
                card_response = VKResponse(self.sdk, self.chat_id)
                card_response.params.update(card)
                self.__query.append((self.sdk.push, {"response": card_response}))
            self.__query[-1][1]['response'].copy_keyboard(self)

    def set_keyboard(self, keyboard: Keyboard):
        self.params['keyboard'] = keyboard.vk_keyboard

    def copy_keyboard(self, instance_from):
        self.params['keyboard'] = instance_from.params['keyboard']

    def platform_based(self):
        if len(self.__query) == 0:
            self.__query.append((self.sdk.push, {'response': self}))
        for command, kwargs in self.__query:
            command(**kwargs)
        return PlainTextResponse('ok')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(self.params)


class VKRequest(AbstractRequest):
    def __init__(self, request: str):
        super(VKRequest, self).__init__(request)
        self.type = self.request.get('type', None)

    @property
    def platform_id(self) -> str:
        return str(self.request['object']['message']['from_id'])

    @property
    def user_id(self) -> str:
        return self.platform_id

    @property
    def user_message(self) -> str:
        return self.request['object']['message']['text']


class VKSDK(AbstractSDK):
    BASE_URL = 'https://api.vk.com/method'
    PLATFORM_NAME = 'VK'

    def __init__(self, token: str, version=5.103):
        super(VKSDK, self).__init__(token)
        self.BASE_PARAMS = {
            'access_token': token,
            'v': version
        }

    @staticmethod
    def is_platform_request(request: dict) -> bool:
        return request.get('type', False) and request.get('object', False)

    @staticmethod
    def parse_request(request: str or dict) -> VKRequest:
        return VKRequest(request)

    def create_response(self, request: VKRequest) -> VKResponse:
        return VKResponse(self, request.platform_id)

    def push(self, response: VKResponse):
        res = httpx.post(f'{self.BASE_URL}/messages.send', data=response.params)
        # logging.info(res.text)

    def upload_file(self, path: str, peer_id=None) -> str or None:
        if is_url(path):
            file = io.BytesIO(httpx.get(path).content)
            file.name = 'file.' + path.split('.')[-1]
        else:
            file = open(path, 'rb')

        if auto_type(path) == 'photo':
            url_response: Any = httpx.get(f'{self.BASE_URL}/photos.getMessagesUploadServer',
                                          params=self.BASE_PARAMS).json()
            url_response = url_response['response']['upload_url']
            publication_response = httpx.post(url_response, files={'photo': file}).json()
            publication_response.update(self.BASE_PARAMS)
            location = httpx.post(f'{self.BASE_URL}/photos.saveMessagesPhoto', data=publication_response).json()
            owner_id, content_id = location['response'][0]['owner_id'], location['response'][0]['id']
            _id = f'photo{owner_id}_{content_id}'

        else:
            params = deepcopy(self.BASE_PARAMS)

            # Костыль, чтобы работала отправка файлов, спасибо ВК
            peer_id = '2000000001' if peer_id is None else peer_id
            params.update({'type': 'doc', 'peer_id': peer_id})
            url_response = httpx.get(f'{self.BASE_URL}/docs.getMessagesUploadServer', params=params).json()
            url_response = url_response['response']['upload_url']
            publication_response = httpx.post(url_response, files={'file': file}).json()
            publication_response.update(self.BASE_PARAMS)
            location: Any = httpx.post(f'{self.BASE_URL}/docs.save', data=publication_response).json()
            owner_id, content_id = location['response']['doc']['owner_id'], location['response']['doc']['id']
            _id = f'doc{owner_id}_{content_id}'
        self.cache_store[path] = _id
        return _id
