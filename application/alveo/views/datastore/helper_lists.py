from .helper_query import datastore_query

def datastore_list(user_id=None, key=None, revision=None):
    if revision is None:
        revision = "latest"

    query_data = datastore_query(user_id=user_id, key=key, revision=revision)
    list_data = []
    for data in query_data:
        list_data.append({
                'key': data.key,
            })

    data = {
                'revision': revision,
                'user_id': user_id,
                'list': list_data
        }

    return data
