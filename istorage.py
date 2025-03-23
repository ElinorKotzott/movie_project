import json
import math
import random
import subprocess
from abc import ABC, abstractmethod
import data_fetcher


class IStorage(ABC):

    def __init__(self, movies, file_path):
        self._movies = movies
        self._file_path = file_path


    def list_movies(self):
        """prints total amount and list of movies"""
        if self._movies is not None:
            print(f"{len(self._movies)} movies in total")
            for movie in self._movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
        return self._movies


    def add_movie(self, title):
        """allows user to add a movie with release year and rating"""
        movie_info = data_fetcher.get_movie_info_by_title(title)
        if movie_info is None:
            return
        if "Error" in movie_info:
            print("Movie not found!")
            return
        title = movie_info["Title"]
        rating = movie_info["imdbRating"]
        year = movie_info["Year"]
        poster_url = movie_info["Poster"]

        if not any(movie["title"] == title for movie in self._movies):
            self._movies.append({"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            self._save_movies()
            print("Movie added successfully!")
        else:
            print("Movie cannot be added because it already exists!")


    def delete_movie(self, title):
        """checks if chosen movie exists and, if yes, deletes it"""
        try:
            self._movies.remove(next((movie for movie in self._movies if movie["title"].lower() == title), -1))
            self._save_movies()
            # returns -1 as default, which will be caught as a value error
            print("The movie has been deleted successfully!")
        except ValueError:
            print("This movie doesn't exist!")


    def update_movie(self, title, rating):
        """allowing user to update movie rating if the desired movie exists in the list"""
        # checking whether the desired movie exists and assigning it to mov, otherwise mov will be None
        to_update = next((movie for movie in self._movies if movie["title"].lower() == title), None)

        if to_update is None:
            return

        to_update["rating"] = rating
        self._save_movies()
        print("The movie has been updated successfully!")


    def print_stats(self):
        amount_of_ratings = len(self._movies)
        ratings_sum = sum([movie["rating"] for movie in self._movies])
        average_rating = round(ratings_sum / amount_of_ratings, 1)
        print(f"The average movie rating is: {average_rating}")

        sorted_ratings = sorted(movie["rating"] for movie in self._movies)
        if len(sorted_ratings) % 2 == 0:
            # calculating median for even numbers
            median_rating = (sorted_ratings[int(len(sorted_ratings) / 2) - 1]
                             + sorted_ratings[int(len(sorted_ratings) / 2)]) / 2
        else:
            # median for odd numbers
            median_rating = sorted_ratings[math.floor(len(sorted_ratings) / 2)]
        print(f"The median rating is: {round(median_rating, 1)}")

        # determining highest and lowest rating
        lowest_rating = min(sorted_ratings)
        highest_rating = max(sorted_ratings)

        # creating list of highest and lowest rated movies with list comprehension
        lowest_rated_movies = [movie["title"] for movie in self._movies if movie["rating"] == lowest_rating]
        highest_rated_movies = [movie["title"] for movie in self._movies if movie["rating"] == highest_rating]

        # printing all of them at the same time with join()
        print(f"The movies with the lowest rating is/are: {', '.join(lowest_rated_movies)}"
              f"with a rating of {lowest_rating}")
        print(f"The movies with the highest rating is/are: {', '.join(highest_rated_movies)}"
              f"with a rating of {highest_rating}")


    def search_movie(self, user_search):
        found = False
        for movie in self._movies:
            if user_search in movie["title"].lower():
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
                found = True
        if not found:
            print("This movie doesn't exist!")


    def print_random_movie(self):
        random_movie = random.choice(self._movies)
        print(f"Your random movie for today is '{random_movie['title']}' "
              f"({random_movie['year']}) with a rating of {random_movie['rating']}")


    def sort_by_rating(self):
        movies_sorted_by_rating_descending = sorted(self._movies, key=lambda movie: movie["rating"], reverse=True)
        for mov in movies_sorted_by_rating_descending:
            print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


    def sort_by_year(self, user_input):
        if user_input == "n":
            movies_sorted_by_year = sorted(self._movies, key=lambda movie: movie["year"])
        if user_input == "y":
            movies_sorted_by_year = sorted(self._movies, key=lambda movie: movie["year"], reverse=True)

        for mov in movies_sorted_by_year:
            print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


    def generate_website(self):
        subprocess.run(['python', 'app.py'])


    @abstractmethod
    def _save_movies(self):
        pass
