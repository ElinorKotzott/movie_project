import csv

from istorage import IStorage


class StorageCSV(IStorage):

    def __init__(self, file_path):
        """instantiates self.movies with csv data"""
        try:
            with (open(file_path, mode="r") as handle):
                reader = csv.DictReader(handle)
                movies = list(reader)
            super().__init__(movies, file_path)
        except FileNotFoundError:
            print("File not found!")
            return


    def _save_movies(self):
        """saves changes by overwriting the current csv file"""
        with open(self._file_path, mode="w") as handle:
            fieldnames = self._movies[0].keys()
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()  # Write header row
            writer.writerows(self._movies)
