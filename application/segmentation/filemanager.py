import os

from application import app

class FileManager:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
    def _validate_path(self):
        """ Validates whether the directory exists or not. Creates the directory if it does not exist. Should not be called from outside the class. """
        directory = os.path.dirname(os.path.realpath(self.filename))
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save(self):
        """ Saves data to the file location. """
        self._validate_path()
        self.data.save(self.filename)
        self.stored = True

    def cleanup(self):
        """ Erases any downloaded data. """
        if self.stored:
            try:
                os.remove(self.filename)
            except:
                pass
            self.stored = False
