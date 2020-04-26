import json
from abc import ABC, abstractmethod
from typing import List
from unibots.components import Keyboard, Card, Gallery


class AbstractResponse(ABC):
    def __init__(self, sdk):
        self.sdk = sdk

    @abstractmethod
    def set_message(self, msg: str):
        pass

    @abstractmethod
    def set_media(self, content: Card or List[Card] or Gallery):
        pass

    @abstractmethod
    def set_keyboard(self, keyboard: Keyboard):
        pass

    def parse_media_args(self, content) -> Card or Gallery:
        error_message = f'You have passed a wrong element to set_media\n' \
                        'Allowed: Card, str(id or path), list of Cards, Gallery, list of str(id or path)'
        if len(content) == 1:
            content = content[0]

        if isinstance(content, str):
            arg = {f'{self.sdk.PLATFORM_NAME.lower()}_id': content} if self.sdk.is_id(content) else {'path': content}
            content = Card(**arg)

        elif isinstance(content, tuple):
            content_buffer = list()
            for element in content:
                if isinstance(element, str):
                    arg = {f'{self.sdk.PLATFORM_NAME.lower()}_id': element} \
                            if self.sdk.is_id(element) else {'path': element}
                    element = Card(**arg)
                elif isinstance(element, Gallery):
                    raise NotImplementedError
                elif not isinstance(element, Card):
                    raise ValueError(error_message)
                content_buffer.append(element)
            content = Gallery(content_buffer)

        assert isinstance(content, Gallery) or isinstance(content, Card), error_message
        return content

    @abstractmethod
    def platform_based(self):
        return

    def __repr__(self):
        return

    def __str__(self):
        return


class AbstractRequest(ABC):
    def __init__(self, request: str or dict):
        if not isinstance(request, dict):
            request = json.loads(request)
        self.request = request  # If it is private, child classes will not see

    @property
    @abstractmethod
    def user_message(self) -> str:
        return ''

    # ID for API
    @property
    @abstractmethod
    def platform_id(self):
        return

    # ID for DB and Session management
    @property
    @abstractmethod
    def user_id(self):
        return

    def __repr__(self):
        return self.request

    def __str__(self):
        return json.dumps(self.request)


class AbstractSDK(ABC):
    BASE_URL = 'https://base.url'
    PLATFORM_NAME = 'Abstract'
    cache_store = dict()

    def __init__(self, token: str):
        self.token = token

    @abstractmethod
    def upload_file(self, path: str) -> str:
        self.cache_store[path] = 'id'
        return 'id'

    @staticmethod
    @abstractmethod
    def is_platform_request(request) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def parse_request(request: str) -> AbstractRequest:
        return AbstractRequest(request)

    @abstractmethod
    def create_response(self, request: AbstractRequest) -> AbstractResponse:
        return AbstractResponse(self)

    def get_file_id(self, path: str) -> str or None:
        return self.cache_store.get(path, None)

    # FIXME Возможно стоит прописать в каждом sdk для точной отработки
    # FIXME Если на какой-то платформе в id будет использоваться ".", то будет работать неправильно!
    @staticmethod
    def is_id(file: str):
        return '.' not in file
