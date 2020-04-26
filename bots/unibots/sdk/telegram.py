import json
import logging
from typing import List, Any

import httpx
from starlette.responses import PlainTextResponse

from unibots.components import Keyboard, Card, Gallery
from unibots.sdk.abstract import AbstractResponse, AbstractRequest, AbstractSDK
from unibots.tools import cut_text, is_url, auto_type


class TelegramResponse(AbstractResponse):
    def __init__(self, sdk, chat_id, message_default: str = 'Бот запущен'):
        super(TelegramResponse, self).__init__(sdk)

        self.message_default = message_default
        self.chat_id = chat_id
        self.method_name = 'sendMessage'
        self.params = {'chat_id': self.chat_id, 'text': self.message_default}

        self.files = None
        self.__used_set = False
        self.__query = list()

    def set_message(self, text: str):
        self.params['text'] = text
        self.method_name = 'sendMessage'

    def edit_message(self, text: str, message_id: int = None):
        self.params['message_id'] = message_id
        self.params['text'] = text
        self.method_name = 'editMessageText'

    def copy_keyboard(self, instance_from):
        self.params['reply_markup'] = instance_from.params.get('reply_markup', dict())

    def set_media(self, *content: Card or Gallery or str):
        self.__query = list()
        content = self.parse_media_args(content)
        if isinstance(content, Card):
            self.__create_file_push(*content.telegram_card, from_gallery=False)
        elif isinstance(content, Gallery):
            self.__create_gallery_push(content.telegram_gallery)

    def __create_gallery_push(self, gallery: Gallery):
        if self.params.get('reply_markup', None) is not None:
            logging.warning('Keyboard will be ignored, because telegram does not support keyboards with gallery')
        upload_images = {}
        media = []
        if gallery.header != '':
            header_response = TelegramResponse(self.sdk, self.chat_id)
            header_response.set_message(gallery.header)
            self.__query.append((self.sdk.push, {'response': header_response}))

        for num, card in enumerate(gallery.cards):
            if card.telegram_id is not None:
                file_type = self.sdk.uploaded_file_type(card.telegram_id)
            elif card.path is not None:
                file_type = auto_type(card.path)
            else:
                logging.warning('The card in gallery does not have fields telegram_id or path, it will be skipped!')
                continue

            if (file_type == 'photo' or file_type == 'video') and not gallery.split:
                if card.telegram_id is not None:
                    media.append({'type': file_type, 'media': card.telegram_id})
                else:
                    if is_url(card.path):
                        media.append({'type': file_type, 'media': card.path})
                    else:
                        upload_images[f'file_{num}'] = open(card.path, 'rb')
                        media.append({'type': file_type, 'media': f'attach://file_{num}'})
            else:
                if card.telegram_id is not None:
                    self.__create_file_push(card.telegram_id, card.caption, file_type)
                elif card.path is not None:
                    self.__create_file_push(card.path, card.caption, file_type)

        if not gallery.split:
            gallery_response = TelegramResponse(self.sdk, self.chat_id)
            gallery_response.params['media'] = json.dumps(media)
            gallery_response.method_name = 'sendMediaGroup'
            gallery_response.files = upload_images
            self.__query.append((self.sdk.push, {'response': gallery_response}))

    def __create_file_push(self, file: str, caption: str = '', file_type: str or None = None, from_gallery=True):
        if from_gallery:
            file_response = TelegramResponse(self.sdk, self.chat_id)
        else:
            file_response = self
        if file_type is None:
            if self.sdk.is_id(file):
                file_type = self.sdk.uploaded_file_type(file)
            else:
                file_type = auto_type(file)

        if not (self.sdk.is_id(file) or is_url(file)):
            file_response.files = {file_type: open(file, 'rb')}
        else:
            file_response.params[file_type] = file
        file_response.method_name = f'send{file_type.capitalize()}'
        file_response.params['caption'] = caption
        if from_gallery:
            self.__query.append((self.sdk.push, {'response': file_response}))

    def set_keyboard(self, keyboard: Keyboard):
        self.params['reply_markup'] = keyboard.telegram_keyboard

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


class TelegramRequest(AbstractRequest):
    @property
    def user_message(self) -> str:
        if self.request.get('message') is not None:
            return self.request['message'].get('text', '')
        else:
            return self.request['callback_query']['data']

    @property
    def platform_id(self) -> str:
        if self.request.get('message') is not None:
            return str(self.request['message']['from']['id'])
        else:
            try:
                return str(self.request['callback_query']['from']['id'])
            except KeyError or IndexError:
                logging.error(f'callback_query not found! {self.request}')

    @property
    def user_id(self):
        return self.platform_id

    @property
    def message_id(self) -> int:
        return self.request['message']['message_id']

    def __repr__(self):
        return self.request

    def __str__(self):
        return json.dumps(self.request)


class TelegramSDK(AbstractSDK):
    BASE_URL = 'https://api.telegram.org/bot'
    PLATFORM_NAME = 'Telegram'
    file_types = dict()

    def __init__(self, token, chat_id, proxies: dict = None):
        super(TelegramSDK, self).__init__(token)
        self.chat_id = chat_id
        self.proxies = proxies

    @staticmethod
    def is_platform_request(request: dict) -> bool:
        return request.get('message', False) and request.get('update_id', False)

    def uploaded_file_type(self, _id):
        file_type = self.file_types.get(_id, 'document')
        if file_type is None:
            logging.warning(f'Haven`t found id: {_id}\n in uploaded files using this instance of sdk.'
                            f'It will be sent as document')
            file_type = 'document'
        return file_type

    @staticmethod
    def parse_request(request: str or dict) -> TelegramRequest:
        return TelegramRequest(request)

    def create_response(self, request: TelegramRequest) -> TelegramResponse:
        return TelegramResponse(self, request.platform_id)

    def __proxy_request(self, url, **kwargs) -> httpx.Response:
        if self.proxies is not None:
            with httpx.Client(proxies=self.proxies) as client:
                response = client.post(url, **kwargs)
        else:
            response = httpx.post(url, **kwargs)
        return response

    def push(self, response: TelegramResponse) -> httpx.Response:
        result = self.__proxy_request(f'{self.BASE_URL}{self.token}/{response.method_name}',
                                      params=response.params, files=response.files)
        return result

    def upload_file(self, path: str) -> str:
        # TODO Добавить проверкук файлов на вес
        file_type = auto_type(path)
        upload_response = TelegramResponse(self, self.chat_id)
        upload_response.set_media(path)

        response = self.push(upload_response).json()
        result = response['result'][file_type]
        if isinstance(result, list):
            result = result[0]
        _id = result['file_id']
        self.cache_store[path] = _id
        self.file_types[_id] = file_type
        return _id
