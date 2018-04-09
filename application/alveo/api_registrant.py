# TODO more elegant solution
#  Ideally do not persistently store AAS API keys for security reasons
API_STORE = {}

def activate_api_access(ats_api_key, aas_api_key):
    API_STORE[ats_api_key] = aas_api_key

def get_api_access(ats_api_key):
    try:
        return API_STORE[ats_api_key]
    except:
        return None

def unregister_api_access(ats_api_key):
    API_STORE[ats_api_key] = None

