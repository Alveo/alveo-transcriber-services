from application import app


def get_domain_handler(module_domain):
    for handler in app.config['DOMAIN_HANDLERS']:
        try:
            if module_domain in handler['domains']:
                return handler['module']
        except BaseException:
            pass


def get_module_metadata(module_domain):
    try:
        return next(
            (handler for handler in app.config['DOMAIN_HANDLERS'] if handler["module"] == module_domain),
            None)
    except BaseException:
        return None
