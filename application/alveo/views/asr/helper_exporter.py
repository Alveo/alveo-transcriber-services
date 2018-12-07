from flask import abort

from application.jobs.model import Job
from application.users.model import User

from application.alveo.module import DOMAIN


def export_asrdata(ds_object):
    return {
        "timestamp": ds_object.timestamp,
        "storage_spec": ds_object.storage_spec,
        "domain": ds_object.key.split[":"][0],
        "asr_engine": ds_object.key.split[":"][1],
        "key": ds_object.key.split[":"][2],
        "transcription": ds_object.get_value()
    }
