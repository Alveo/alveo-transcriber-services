from flask.views import MethodView

from application.session import auth_required

class AlveoAuthSegmentor(MethodView):
    @auth_required
    def get(self, identifier=None):
        document_id = request.args.get('document_id')
