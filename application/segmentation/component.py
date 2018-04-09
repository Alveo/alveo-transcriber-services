import uuid
from urllib.parse import urlparse

from flask import jsonify, abort, g, request
from flask.views import MethodView

from application import app, db
from application.filemanager import FileManager
from application.segmentation.audio_segmentor import AudioSegmentor
from application.segmentation.cache.model import cache_result, get_cached_result
from application.users.auth import auth_required, get_api_access

segmentor_service = SegmentorService.as_view('segmentor_service')
