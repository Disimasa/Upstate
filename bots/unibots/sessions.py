import logging
from time import time
from asyncio import sleep

from unibots.events import EventManager


class Session:
    def __init__(self, session_id, path, default_global_store=None, inactive_life_time=600):
        if default_global_store is None:
            default_global_store = dict()

        self.__global_store = default_global_store
        self.__local_store = dict()
        self.__current_path = path

        self.last_time_used = time()
        self.inactive_life_time = inactive_life_time
        self.session_id = session_id

    def redirect(self, new_path: str):
        self.__current_path = new_path
        self.local_store = dict()

    @property
    def current_path(self):
        self.last_time_used = time()
        return self.__current_path

    @current_path.setter
    def current_path(self, value):
        self.last_time_used = time()
        self.__current_path = value

    @property
    def global_store(self):
        self.last_time_used = time()
        return self.__global_store

    @global_store.setter
    def global_store(self, value):
        self.last_time_used = time()
        self.__global_store = value

    @property
    def local_store(self):
        self.last_time_used = time()
        return self.__local_store

    @local_store.setter
    def local_store(self, value):
        self.last_time_used = time()
        self.__local_store = value


class SessionManager:
    def __init__(self,
                 session_start_path: str = '/',
                 default_global_storage: dict or None = None,
                 check_inactive_sessions_after: int = 600):

        self.event_manager = EventManager()
        self.sessions_storage = dict()
        self.check_inactive_sessions_after = check_inactive_sessions_after

        self.session_start_path = session_start_path
        self.default_global_storage = default_global_storage

    def create_new_session(self, platform_id: str) -> Session:
        new_session = Session(platform_id, self.session_start_path, self.default_global_storage)
        self.sessions_storage[platform_id] = new_session
        return new_session

    def get_session(self, platform_id: str, create_new=True):
        if platform_id not in self.sessions_storage:
            if create_new:
                self.event_manager.generate_event('new_session', platform_id)
                return self.create_new_session(platform_id)
            return None
        return self.sessions_storage[platform_id]

    async def run_sessions_destroyer(self):
        while True:
            await sleep(self.check_inactive_sessions_after)
            counter = 0
            deleting_sessions = dict()
            for key, element in self.sessions_storage.items():
                if hasattr(element, 'last_time_used') and hasattr(element, 'inactive_life_time'):
                    if time() - element.last_time_used > element.inactive_life_time:
                        counter += 1
                        deleting_sessions[key] = self.sessions_storage[key]
                else:
                    logging.warning('The element doesnt have attrs: last_time_used and/or '
                                    'inactive_life_time. It will not be deleted!')
            self.event_manager.generate_event('deleting_sessions', deleting_sessions)
            for key, value in deleting_sessions.items():
                del self.sessions_storage[key]
            logging.info(f'Destroyed: {counter} session(s)')
