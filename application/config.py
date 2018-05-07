import os

class Environment(object):
    # Will be disabled by default in future releases
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    ACCESS_CONTROL_ALLOW_ORIGIN = os.environ.get('ACCESS_CONTROL_ALLOW_ORIGIN', '*')

    """
        Set the aggressivenses of the SSAD module.

        See https://github.com/wiseman/py-webrtcvad for more information.
    """
    SSAD_AGGRESSIVENESS = os.environ.get('SSAD_AGGRESSIVENSES', 2)

    """
        Enable or disable POST-based segmentation.

        POSTs should be authenticated by a module, so disabling this is usually unnecessary.
    """
    ALLOW_POST_SEGMENTATION = os.environ.get('ALLOW_POST_SEGMENTATION', True)

    """
        Set RequestEntityTooLarge threshold.

        Set in bytes.

        This should be large enough to accept files, assuming POST based segmentation is allowed.
        Where POST based segmentation is disabled, this should typically be set to about 1 megabyte.
    """
    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH', 40 * 1024 * 1024) # 40 MB

    """
        Set the cache path.

        Used for temporary storage of:
            POST files
            Downloaded cache from modules (e.g PyAlveo)

        Recommended to use the /tmp/ directory
    """
    DOWNLOAD_CACHE_PATH = os.environ.get('DOWNLOAD_CACHE_PATH', '/tmp/alveo-transcriber-services/alveo/') # Used for downloaded audio files including POST requests

    """
        Set the modules for domain handling

        You shouldn't touch this unless you know what you're doing
    """
    DOMAIN_HANDLERS = os.environ.get('DOMAIN_HANDLERS', [
      {
        'domains': ['app.alveo.edu.au'],
        'module': 'alveo', # Comment out this line if you wish to disable the Alveo API
        'api_url': 'https://app.alveo.edu.au/'
      }
    ])
