import uuid

from flask import g
from application.auth.required import auth_required
from .api_rate_limiter import api_rate_limiter

from application import app, events

MODULE_PATHS = {
    'AUTH': 'auth',
    'SEGMENTATION': 'segmenter',
    'DATASTORE': {
        'EXPORT': {
            'SELF': 'datastore:export',
            'USER': 'datastore:export_by_user',
            'KEY': 'datastore:export_by_key',
            'USER+KEY': 'datastore:export_by_user_key',
        },
        'LIST': {
            'SELF': 'datastore:list',
            'USER': 'datastore:list_by_user',
            'KEY': 'datastore:list_by_key',
            'USER+KEY': 'datastore:list_by_user_key',
        },
        'GET': 'datastore:get',
        'POST': 'datastore:post'
    }
}
class handle_api_event(object):
    def __init__(self, module_id, event_name, rate_limit=None, auth_required=False):
        self.set_limiter(rate_limit)
        self.auth_required = auth_required
        self.register(module_id, event_name);

    def set_limiter(self, limit_args):
        self.rate_limit = limit_args

    def register(self, module_id, event_name):
        if not module_id in events:
            events.update({module_id: {}})

        events[module_id][event_name] = self

    def __call__(self, function):
        if self.auth_required is True:
            function = auth_required(function)

        if self.rate_limit != None:
            print("limited")
            from application import limiter
            function = limiter.limit(self.rate_limit)(function)

        self.handle = function

class register_module_rule(object):
    def __init__(
        self,
        module_name,
        url,
        methods=['GET'],
        endpoint=str(uuid.uuid4()),
        prehandler=None):

        if module_name in [None, ""]:
            raise Exception("Failed to register a module rule as the module_name is invalid.")
        self.module_name = module_name

        if url in [None, ""]:
            raise Exception("Failed to register a module rule as the url is invalid.")
        self.url = url

        self.endpoint = endpoint
        self.methods = methods
        self.prehandler = prehandler 

        if self.prehandler != None:
            self.register(module_name, prehandler);

    def register(self, module_id, event_name):
        if not module_id in events:
            events.update({module_id: {}})

        events[module_id][event_name] = self

    def __call__(self, view_func):
        if self.prehandler != None:
            self.handle = view_func
            view_func = self.prehandler;
            view_func.post = self
            view_func = view_func.as_view('ds_api_export')
        
        path = '/%s%s' % (self.module_name, self.url)
        app.add_url_rule(path, view_func=view_func, methods=self.methods, endpoint=self.endpoint)

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
