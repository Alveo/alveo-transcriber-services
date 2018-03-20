import sndhdr

from application import app
from application.segmentation.speechtools import sad

class AudioSegmentor:
    """ AudioSegmentor is a class for validating and segmenting wave files. """
    def __init__(self, wave_file):
        self.wave_file = wave_file

        self._validate()

    def _validate(self):
        """ Determines whether the file is a valid wave file. Should not be called from outside the class. """
        self.valid = False
        header = sndhdr.whathdr(self.wave_file);

        if header is not None:
            if header.filetype is "wav":
                self.valid = True

    def isValid(self):
        """ Returns if the file has been confirmed as a valid wave file. """
        return self.valid

    def segment(self):
        """ Returns SSAD information as JSON. """
        return sad(self.wave_file, app.config['SSAD_AGGRESSIVENESS'])
