import os

from application import app


class FileManager:
    def __init__(self, file_path, file_data):
        self.file_path = file_path
        self._validate_path()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file_data)

        self.stored = True

    def _validate_path(self):
        """ Validates whether the directory exists or not. Creates the directory if it does not exist. Should not be called from outside the class. """
        directory = os.path.dirname(os.path.realpath(self.file_path))
        if not os.path.exists(directory):
            os.makedirs(directory)

    def cleanup(self):
        """ Erases any downloaded data. """
        if self.stored:
            try:
                os.remove(self.file_path)
            except BaseException:
                pass
            self.stored = False
