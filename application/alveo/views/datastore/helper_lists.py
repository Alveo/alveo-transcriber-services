from .helper_query import datastore_query

def datastore_list(user_id=None, key=None, revision=None):
    if revision == None:
        revision = "latest"

    query_data = datastore_query(user_id=user_id, key=key, revision=revision)
    list_data = []
    for data in query_data:
        list_data.append({
                'id': data.id,
            })

    data = {
                'query_revision': revision,
                'query_user_id': user_id,
                'query_key': key,
                'storage_objects': list_data
        }

    return data
