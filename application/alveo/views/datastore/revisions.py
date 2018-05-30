from flask import abort

from application.users.model import User

from application.datastore.model import Datastore

from application.alveo.module import DOMAIN, SUPPORTED_STORAGE_KEYS

from application.auth.required import auth_required
from application.datastore.view_wrappers.revisions import RevisionsWrapper

from application import limiter


class AlveoRevisionsRoute(RevisionsWrapper):
    decorators = [
        auth_required,
        limiter.limit("30 per minute"),
        limiter.limit("1000 per hour"),
        limiter.limit("5000 per day")
    ]

    def _processor_get(self, store_id, user_id):
        query = Datastore.query.filter(Datastore.id == store_id).first()

        if query is None:
            abort(404, 'No match for the provided id')

        user = User.query.filter(User.id == query.user_id).first()

        if not user.domain == DOMAIN:
            abort(
                403,
                'You don\'t have permission to read the storage of an external user')

        revision_list = []
        for version in query.versions:
            revision_list.append(version.revision)

        return {
            'id': query.id,
            'total_revisions': len(revision_list),
            'revisions': revision_list
        }


revisions_route = AlveoRevisionsRoute.as_view('/alveo/datastore/revisions/')
