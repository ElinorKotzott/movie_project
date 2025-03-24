import json

from storage.istorage import IStorage


class StorageJson(IStorage):

    def __init__(self, file_path):
        """instantiates self.movies with json data"""
        try:
            with open(file_path, "r") as handle:
                movies = json.load(handle)
        except  (json.JSONDecodeError, FileNotFoundError):
            print("File not found or empty - starting with empty movies file")
            movies = []
        super().__init__(movies, file_path)


    def _save_movies(self):
        """saves changes by overwriting the current json file"""
        with open(self._file_path, "w") as handle:
            json.dump(self._movies, handle)
