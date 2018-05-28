import os
import json


def eval_bool(boolean):
    return str(boolean).lower() in ("true", "1")


class Environment(object):
    # Will be disabled by default in future releases
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = False


class ProductionEnvironment(Environment):
    """
        Set up a production environment.
    """

    """
        Set the database path.

        This also matches Dokku's automatically set database environment variable.

        Examples:
         'sqlite:////tmp/test.db'
         'postgres://devuser:devpassword@localhost/alveots'
         'mysql://devuser:devpassword@localhost/alveots'
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)

    """
        Set allowed origins.

        Allows applications to access this API if hosted on a different domain
        By default as this is an API service, there is no access control set.
    """
    ACCESS_CONTROL_ALLOW_ORIGIN = os.environ.get(
        'ACCESS_CONTROL_ALLOW_ORIGIN', '*')

    """
        Set the aggressivenses of the SSAD module.

        See https://github.com/wiseman/py-webrtcvad for more information.
    """
    SSAD_AGGRESSIVENESS = int(os.environ.get('SSAD_AGGRESSIVENSES', "2"))

    """
        Enable or disable POST-based segmentation.

        POSTs should be authenticated by a module, so disabling this is usually unnecessary.
    """
    ALLOW_POST_SEGMENTATION = eval_bool(
        os.environ.get('ALLOW_POST_SEGMENTATION', True))

    """
        Set RequestEntityTooLarge threshold.

        Set in bytes. Default is 40MB.

        This should be large enough to accept files, assuming POST based segmentation is allowed.
        Where POST based segmentation is disabled, this should typically be set to about 1 megabyte.
    """
    MAX_CONTENT_LENGTH = int(os.environ.get(
        'MAX_CONTENT_LENGTH', 40 * 1024 * 1024))

    """
        Set the cache path.

        Used for temporary storage of:
            POST files
            Downloaded cache from modules (e.g PyAlveo)

        Recommended to use the /tmp/ directory
    """
    DOWNLOAD_CACHE_PATH = os.environ.get(
        'DOWNLOAD_CACHE_PATH', '/tmp/alveo-transcriber-services/alveo/')

    """
        Set the modules for domain handling

        You shouldn't touch this unless you know what you're doing

        Modules can be disabled by removing their entry from the list.
    """
    DOMAIN_HANDLERS = json.loads(
        os.environ.get('DOMAIN_HANDLERS', '[ \
                { \
                    "domains": ["app.alveo.edu.au"], \
                    "module": "alveo", \
                    "api_url": "https://app.alveo.edu.au/" \
                } \
            ]')
    )


class TestEnvironment(ProductionEnvironment):
    TESTING = True
