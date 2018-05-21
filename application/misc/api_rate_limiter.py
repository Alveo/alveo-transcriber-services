from application import limiter

def api_rate_limiter(f, f_args):
    """ Provides a wrapper for views to enforce login requirements """
    print(f_args)
    @limiter.limit(**f_args)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
