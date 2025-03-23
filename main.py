from movie_app import MovieApp
from storage_csv import StorageCSV
from storage_json import StorageJson


# storage = StorageCSV('movies.csv')
storage = StorageJson('movies.json')
if storage is not None:
    movie_app = MovieApp(storage)
    movie_app.run()
