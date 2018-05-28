from flask.views import MethodView


class QueryWrapper(MethodView):
    def _processor_get(self, **args):
        raise NotImplementedError

    def _processor_put(self, **args):
        raise NotImplementedError

    def _processor_post(self, **args):
        raise NotImplementedError

    def _processor_delete(self, **args):
        raise NotImplementedError
