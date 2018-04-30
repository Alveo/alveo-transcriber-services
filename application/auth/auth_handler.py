from application import auth_handlers

class register_auth_handler(object):
    def __init__(self, name):
        self.auth_name = name
        self.register();

    def register(self):
        auth_handlers.append(self)

    def __call__(self, function):
        self.authenticate = function
