import json
import math

from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        """instantiates self.movies with json data"""
        try:
            with open(file_path, "r") as my_fileobj:
                movies = json.load(my_fileobj)
            self.movies = movies
        except FileNotFoundError:
            self.movies = None


    def list_movies(self):
        """prints total amount and list of movies"""
        if self.movies is not None:
            print(f"{len(self.movies)} movies in total")
            for movie in self.movies:
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


    def add_movie(self, title, year, rating, poster):
        """allows user to add a movie with release year and rating"""
        self.movies.append({"title": title, "year": year, "rating": rating})
        self.__save_movies()
        print("Movie added successfully!")



    def delete_movie(self, title):
        """checks if chosen movie exists and, if yes, deletes it"""
        try:
            self.movies.remove(next((movie for movie in self.movies if movie["title"].lower() == title), -1))
            self.__save_movies()
            # returns -1 as default, which will be caught as a value error
            print("The movie has been deleted successfully!")
        except ValueError:
            print("This movie doesn't exist!")


    def update_movie(self, title, rating):
        """allowing user to update movie rating if the desired movie exists in the list"""
        to_update = input("Which movie would you like to update? ").lower()
        # checking whether the desired movie exists and assigning it to mov, otherwise mov will be None
        mov = next((movie for movie in self.movies if movie["title"].lower() == to_update), None)

        if mov is None:
            return

        while True:
            print("Please enter a new rating! ")
            try:
                new_rating = float(input(""))
                mov["rating"] = new_rating
                self.__save_movies()
                print("The movie has been updated successfully!")
                break
            except ValueError:
                print("Invalid rating! ")

    def print_stats(self):
        amount_of_ratings = len(self.movies)
        ratings_sum = sum([movie["rating"] for movie in self.movies])
        average_rating = round(ratings_sum / amount_of_ratings, 1)
        print(f"The average movie rating is: {average_rating}")

        sorted_ratings = sorted(movie["rating"] for movie in self.movies)
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
        lowest_rated_movies = [movie["title"] for movie in self.movies if movie["rating"] == lowest_rating]
        highest_rated_movies = [movie["title"] for movie in self.movies if movie["rating"] == highest_rating]

        # printing all of them at the same time with join()
        print(f"The movies with the lowest rating is/are: {', '.join(lowest_rated_movies)}"
              f"with a rating of {lowest_rating}")
        print(f"The movies with the highest rating is/are: {', '.join(highest_rated_movies)}"
              f"with a rating of {highest_rating}")

    def __search_movie(self, user_search):
        found = False
        for movie in self.movies:
            if user_search in movie["title"].lower():
                print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
                found = True
        if not found:
            print("This movie doesn't exist!")


    def __save_movies(self):
        """saves changes by overwriting the current json file"""
        with open("data.json", "w") as handle:
            json.dump(self.movies, handle)
