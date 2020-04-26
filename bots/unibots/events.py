import logging


class EventManager:
    POSSIBLE_EVENTS = ['new_session', 'new_request', 'deleting_sessions']

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventManager, cls).__new__(cls)
            cls.instance.subscriptions = dict()
        return cls.instance

    def make_subscription(self, event_type):
        def wrapper(func):
            self.instance.subscriptions[event_type] = self.instance.subscriptions.get(event_type, list()) + [func]
        return wrapper

    def generate_event(self, event_type, *args, **kwargs):
        subscribers = self.instance.subscriptions.get(event_type, list())
        logging.info(f'Event {event_type} was generated. Subscribers triggered: {len(subscribers)}')
        for sub in subscribers:
            sub(*args, **kwargs)