from .helper_query import datastore_query


def datastore_list(user_id=None, object_key=None):
    query_data = datastore_query(user_id=user_id, key=object_key)
    list_data = []
    for data in query_data:
        total_versions = data.versions.count()
        list_data.append({
            'id': data.id,
            'version': total_versions - 1,
            'total_versions': total_versions,
            'timestamp': data.timestamp.isoformat()
        })

    data = {
        'storage_objects': list_data
    }

    return data
