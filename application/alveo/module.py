DOMAIN = "alveo"

SUPPORTED_STORAGE_KEYS = {
    'start': {
        'type': float,
        'required': True
    },
    'end': {
        'type': float,
        'required': True
    },
    'speaker': {
        'type': str,
        'required': True
    },
    'annotation': {
        'type': str,
        'required': True
    }
}
