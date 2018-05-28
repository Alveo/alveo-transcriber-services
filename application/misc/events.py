from flask import g

from application import app, events

EVENTS = {
    'AUTH': 'auth'
}

class handle_api_event(object):
    def __init__(self, module_id, event_name):
        self.register(module_id, event_name)

    def register(self, module_id, event_name):
        if not module_id in events:
            events.update({module_id: {}})

        events[module_id][event_name] = self

    def __call__(self, function):
        self.handle = function

def get_domain_handler(domain):
    for handler in app.config['DOMAIN_HANDLERS']:
        try:
            if domain in handler['domains']:
                return handler['module']
        except:
            pass

def get_module_metadata(module):
    try:
        return next((handler for handler in app.config['DOMAIN_HANDLERS'] if handler["module"] == module), None)
    except:
        return None

def get_handler_for(domain, event):
    module = get_domain_handler(domain)
    if module is None:
        return None

    handler_ref = None
    try:
        handler_ref = events[module][event]
    except:
        pass

    return handler_ref
