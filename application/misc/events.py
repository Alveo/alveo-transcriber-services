from flask import g

from application import events
from .modules import get_domain_handler

EVENTS = {
    'AUTH': 'auth'
}


class handle_api_event(object):
    def __init__(self, module_id, event_name):
        self.register(module_id, event_name)

    def register(self, module_id, event_name):
        if module_id not in events:
            events.update({module_id: {}})

        events[module_id][event_name] = self

    def __call__(self, function):
        self.handle = function


def get_handler_for(domain, event):
    module = get_domain_handler(domain)
    if module is None:
        return None

    handler_ref = None
    try:
        handler_ref = events[module][event]
    except BaseException:
        pass

    return handler_ref
