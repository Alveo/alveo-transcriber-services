from application import limiter

def rate_limit(f, limit_value):
    """ Provides a wrapper for views to enforce login requirements """
    @limiter.limit(limit_value)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
