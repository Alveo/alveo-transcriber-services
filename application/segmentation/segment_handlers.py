from application import segment_handlers

class register_segmenter(object):
    def __init__(self, name):
        self.name = name
        self.register();

    def register(self):
        segment_handlers.append(self)

    def __call__(self, function):
        self.segment = function
