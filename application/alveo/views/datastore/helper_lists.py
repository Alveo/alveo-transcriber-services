from .helper_query import datastore_query


def datastore_list(user_id=None, object_key=None):
    query_data = datastore_query(user_id=user_id, key=object_key)
    list_data = []
    for data in query_data:
        list_data.append({
            'id': data.id,
        })

    data = {
        'storage_objects': list_data
    }

    return data
