import sndhdr

import uuid

from application import app
from application.segmentation.speechtools.segmentor import sad
from application.datastore.filemanager import FileManager


def segment_audio_data(audio_data):
    file_path = app.config['DOWNLOAD_CACHE_PATH'] + str(uuid.uuid4())

    downloader = FileManager(file_path, audio_data)

    # Attempt to segment the file
    processor = AudioSegmentor(file_path)
    if not processor.isValid():
        return None

    result = processor.segment()

    # Cleanup after segmenting
    downloader.cleanup()

    return result


class AudioSegmentor:
    """ AudioSegmentor is a class for validating and segmenting wave files. """

    def __init__(self, wave_file):
        self.wave_file = wave_file

        self._validate()

    def _validate(self):
        """ Determines whether the file is a valid wave file. Should not be called from outside the class. """
        self.valid = False
        header = sndhdr.whathdr(self.wave_file)

        if header is not None:
            if header.filetype is "wav":
                self.valid = True

    def isValid(self):
        """ Returns if the file has been confirmed as a valid wave file. """
        return self.valid

    def segment(self):
        """ Returns SSAD information as JSON. """
        return sad(self.wave_file, app.config['SSAD_AGGRESSIVENESS'])
