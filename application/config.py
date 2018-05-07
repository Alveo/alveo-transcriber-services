import os

class Environment(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionEnvironment(Environment):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)

    ACCESS_CONTROL_ALLOW_ORIGIN = os.environ.get('ACCESS_CONTORL_ALLOW_ORIGIN', '')

    SSAD_AGGRESSIVENESS = os.environ.get('SSAD_AGGRESSIVENSES', 2)

    ALLOW_POST_SEGMENTATION = os.environ.get('ALLOW_POST_SEGMENTATION', True)

    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH', 40 * 1024 * 1024) # After 40mb, throw RequestEntityTooLarge exception. You should shrink this down if ALLOW_POST_SEGMENTATION is False

    DOWNLOAD_CACHE_PATH = os.environ.get('DOWNLOAD_CACHE_PATH', '/tmp/alveo-transcriber-services/alveo/') # Used for downloaded audio files including POST requests

    DOMAIN_HANDLERS = os.environ.get('DOMAIN_HANDLERS', [
      {
        'domains': ['app.alveo.edu.au'],
        'module': 'alveo', # Comment out this line if you wish to disable the Alveo API
        'api_url': 'https://app.alveo.edu.au/'
      }
    ])
