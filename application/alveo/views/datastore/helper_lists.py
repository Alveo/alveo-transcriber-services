from .helper_query import datastore_query

def datastore_list(user_id=None, key=None, revision=None):
    data = {
                'revision': revision,
                'list': datastore_query(user_id=user_id, key=key, revision=revision)
        }

    return data
