import io
import os
import sys
from uuid import uuid4

import six
from google.cloud.speech import enums
from google.cloud.speech import types

from application import gce_speech_client, gce_storage_client

def gcloud_transcribe_short(config):
    """
    Uses Google Cloud Speech-to-Text to transcribe audio files up 
    to durations of 60 seconds.

    @config: Provided as a dict, requires at minimum:
        - file_location - /path/to/file
        - sample_rate_hertz - gcloud setting, typically 16000
        - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
        - encoding - gcloud setting, e.g 
                        enums.RecognitionConfig.AudioEncoding.LINEAR16

        Other examples of config options that might be of use:
        - enable_speaker_diarization=False, diarization_speaker_count=2):
        - enable_word_time_offsets=False

    @return: Response object from Google Cloud Speech
    """
    try:
        audio_data = config.pop('audio_data')
    except KeyError:
        raise KeyError("`audio_data` not specified for transcription operation.")

    # Read file into memory before uploading
    audio = types.RecognitionAudio(content=audio_data)
    
    # Detects speech in the audio file
    return gce_speech_client.recognize(config, audio)

def gcloud_transcribe_long(config):
    """
    Uses Google Cloud Speech-to-Text to transcribe audio files beyond
    a duration of 60 seconds. Note that files must be uploaded to Google-
    -Cloud Storage (GCS) before this can be ran. See `gcloud_upload_file`
    for more information.

    @config: Provided as a dict, requires at minimum:
        - file_location - path to gs://bucket_name/file_location
        - sample_rate_hertz - gcloud setting, typically 16000
        - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
        - encoding - gcloud setting, e.g 
                        enums.RecognitionConfig.AudioEncoding.LINEAR16
        - timeout - how long to wait before timing out

        Other examples of config options that might be of use:
        - enable_speaker_diarization=False, diarization_speaker_count=2):
        - enable_word_time_offsets=False

    @return: Response object from Google Cloud Speech
    """
    try:
        audio_data = config.pop('audio_data')
    except KeyError:
        raise KeyError("`audio_data` not specified for transcription operation.")

    try:
        timeout = config.pop('timeout')
    except KeyError:
        raise KeyError("`timeout` not specified for transcription operation.")

    audio = types.RecognitionAudio(uri=audio_data)
    operation = gce_speech_client.long_running_recognize(config, audio)

    response = operation.result(timeout=timeout)

    return response

def gcloud_upload_file(audio_data, gcloud_bucket_name):
    """
    Uploads a single file to GCloud Storage in the specified
    bucket.

    @local_filepath: /path/to/file/to/be/uploaded
    @gcloud_bucket_name: remote bucket name set up via GCloud

    @return: remote url of the uploaded file
    """
    bucket = gce_storage_client.get_bucket(gcloud_bucket_name)
    remote_filepath = "%s" % uuid4()

    blob = bucket.blob(remote_filepath)

    # Upload the audio
    blob.upload_from_string(audio_data)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

def gcloud_delete_file(file_name, gcloud_bucket_name):
    """Deletes a blob from the bucket."""
    bucket = gce_storage_client.get_bucket(gcloud_bucket_name)
    blob = bucket.blob(file_name)

    blob.delete()

def transcribe(config):
    """
    Automatically handles the interaction with Google Speech-to-text in order to
     automagically transcribe some audio data.

    GCloud requires a different mechanism if the audio file is longer than 60 seconds,
     we can save a few steps and have the operation complete quicker if it is less than
     that specified duration though.

    If the file is longer than 60 seconds, it has be uploaded to GCloud Storage, so
     this function will take care of that for us.

    @config: Provided as a dict, requires at minimum:
        - file_location - path to gs://bucket_name/file_location
        - timeout - how long to wait before timing out
        - sample_rate_hertz - gcloud setting, typically 16000
        - language_code - gcloud setting, e.g 'en-AU' or 'ja-JP'
        - encoding - gcloud setting, e.g 
                        enums.RecognitionConfig.AudioEncoding.LINEAR16

        Other examples of config options that might be of use:
        - audio_duration - duration of the audio file to be transcribed in seconds
                            Not required but should be specified for files less than
                            60 seconds in duration as there is a slightly quicker way
                            to have them transcribed.
        - enable_speaker_diarization=False, diarization_speaker_count=2):
        - enable_word_time_offsets=False

    @return: The transcribed data
    """

    long_mode = True

    if 'audio_data' not in config:
        raise KeyError("`audio_data` not specified for transcription operation.")

    if 'timeout' not in config:
        raise KeyError("`timeout` not specified for transcription operation.")

    try:
        if config.pop('audio_duration') < 60: 
            long_mode = False
    except KeyError:
        pass

    if long_mode:
        print("Running in long audio duration mode (audio is >60 seconds duration)...")
        print("Uploading file...")
        remote_object = gcloud_upload_file(config['audio_data'], config['storage_bucket'])
        file_name = remote_object.rsplit('/', 1)[-1]

        config['audio_data'] = "gs://%s/%s" % (config['storage_bucket'], file_name)
        storage_bucket = config.pop('storage_bucket')

        print("Transcribing file...")
        result = gcloud_transcribe_long(config)

        print("Transcription successful, cleaning up...")
        print("Deleting uploaded GCS file...")
        gcloud_delete_file(file_name, storage_bucket)
    else:
        print("Transcribing file...")
        config.pop('timeout')
        config.pop('storage_bucket')
        result = gcloud_transcribe_short(config)

    return result