import math
import random
import sys
import json


def main():
    #movies are loaded from the json file
    movies = load_movies("data.json")
    print_header()
    while True:
        display_menu()
        user_choice = (input("Enter a number between 0 and 10: "))
        try:
            determine_user_choice(user_choice, movies)
        except KeyError:
            print("Invalid option. Please choose a number between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def load_movies(filename):
    """loads movies from the data.json file"""
    try:
        with open(filename, "r") as my_fileobj:
            movies = json.load(my_fileobj)
        return movies
    except FileNotFoundError:
        return -1


def save_movies(movies):
    """saves changes by overwriting the current json file"""
    with open("data.json", "w") as my_fileobj:
        json.dump(movies, my_fileobj)


def print_header():
    """prints program header"""
    print("*" * 10 + " My Movies Database " + "*" * 10)


def display_menu():
    """printing menu"""
    print()
    print("Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
          "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
          "8. Movies sorted by rating\n9. Movies sorted by year\n10. Filter movies")
    print()


def list_movies(movies):
    """prints total amount and list of movies"""
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


def add_movie(movies):
    """allows user to add a movie with release year and rating"""
    title = input("Please enter the movie name! ")
    if not any(movie["title"] == title for movie in movies):
        print("Please enter the year! ", end="")
        while True:
            try:
                year = int(input(""))
                break
            except ValueError:
                print("Please enter a number! ")

        print("Please enter the movie rating! ", end="")
        while True:
            try:
                rating = float(input(""))
                break
            except ValueError:
                print("Please enter a number! ")

        movies.append({"title": title, "year": year, "rating": rating})
        save_movies(movies)
        print("Movie added successfully!")
    else:
        print("Movie already exists! Do you want to update it? Press 4 to update!")


def delete_movie(movies):
    """checks if chosen movie exists and, if yes, deletes it"""
    try:
        to_delete = input("Which movie would you like to delete? ").lower()
        movies.remove(next((movie for movie in movies if movie["title"].lower() == to_delete), -1))
        save_movies(movies)
        #returns -1 as default, which will be caught as a value error
        print("The movie has been deleted successfully!")
    except ValueError:
        print("This movie doesn't exist!")


def update_movie(movies):
    """allowing user to update movie rating if the desired movie exists in the list"""
    to_update = input("Which movie would you like to update? ").lower()
    #checking whether the desired movie exists and assigning it to mov, otherwise mov will be None
    mov = next((movie for movie in movies if movie["title"].lower() == to_update), None)

    if mov is None:
        #movie is called "mov" here because otherwise it shadowed a name
        return

    while True:
        print("Please enter a new rating! ")
        try:
            new_rating = float(input(""))
            mov["rating"] = new_rating
            save_movies(movies)
            print("The movie has been updated successfully!")
            break
        except ValueError:
            print("Invalid rating! ")


def print_stats(movies):
    """calculating and printing average, median and lowest and highest ratings"""
    #summing up, dividing by length and printing average
    amount_of_ratings = len(movies)
    ratings_sum = sum([movie["rating"] for movie in movies])
    average_rating = round(ratings_sum / amount_of_ratings, 1)
    print(f"The average movie rating is: {average_rating}")

    sorted_ratings = sorted(movie["rating"] for movie in movies)
    if len(sorted_ratings) % 2 == 0:
        #calculating median for even numbers
        median_rating = (sorted_ratings[int(len(sorted_ratings) / 2) - 1]
        + sorted_ratings[int(len(sorted_ratings) / 2)]) / 2
    else:
        #median for odd numbers
        median_rating = sorted_ratings[math.floor(len(sorted_ratings) / 2)]
    print(f"The median rating is: {round(median_rating, 1)}")

    #determining highest and lowest rating
    lowest_rating = min(sorted_ratings)
    highest_rating = max(sorted_ratings)

    #creating list of highest and lowest rated movies with list comprehension
    lowest_rated_movies = [movie["title"] for movie in movies if movie["rating"] == lowest_rating]
    highest_rated_movies = [movie["title"] for movie in movies if movie["rating"] == highest_rating]

    #printing all of them at the same time with join()
    print(f"The movies with the lowest rating is/are: {', '.join(lowest_rated_movies)}"
    f"with a rating of {lowest_rating}")
    print(f"The movies with the highest rating is/are: {', '.join(highest_rated_movies)}"
    f"with a rating of {highest_rating}")


def print_random_movie(movies):
    """choosing and printing a random movie from the movies list"""
    random_movie = random.choice(movies)
    print(f"Your random movie for today is '{random_movie['title']}' "
          f"({random_movie['year']}) with a rating of {random_movie['rating']}")


def search_movie(movies):
    """allows user to search movies using a part of the title"""
    user_search = input("Please type a part of the movie title! ").lower()
    found = False
    for movie in movies:
        if user_search in movie["title"].lower():
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
            found = True
    if not found:
        print("This movie doesn't exist!")


def sort_by_year(movies):
    """sorting our movies list ascending or descending depending on the user's choice"""
    print("Do you want the latest movies first? (Y/N)")
    while True:
        user_input = input("").lower()
        if user_input == "n":
            movies_sorted_by_year = sorted(movies, key=lambda movie: movie["year"])
            break
        if user_input == "y":
            movies_sorted_by_year = sorted(movies, key=lambda movie: movie["year"], reverse=True)
            break
        print("Invalid input. Enter 'Y' or 'N'! ")

    for mov in movies_sorted_by_year:
        print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


def sort_by_rating(movies):
    """prints movies sorted by rating, descending"""
    movies_sorted_by_rating_descending = sorted(movies,
    key=lambda movie: movie["rating"], reverse=True)
    for mov in movies_sorted_by_rating_descending:
        print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


def filter_movies(movies):
    """prints movies that fulfill conditions defined by user"""
    print("Enter minimum rating - leave blank for no minimum rating ")
    minimum_rating = validate_input(float)

    print("Enter start year - leave blank for no start year! ")
    start_year = validate_input(int)

    print("Enter end year - leave blank for no end year! ")
    end_year = validate_input(int)

    #creating list of movies that fit the criteria defined by the user
    valid_movies = [movie for movie in movies if (minimum_rating is None
                    or movie["rating"] >= minimum_rating)
                    and (start_year is None or start_year <= movie["year"])
                    and (end_year is None or movie["year"] <= end_year)]

    for valid_movie in valid_movies:
        print(f"{valid_movie['title']} ({valid_movie['year']}): {valid_movie['rating']}")


def validate_input(data_type):
    while True:
        user_input = input("")
        if user_input == "":
            number = None
            break
        try:
            number = data_type(user_input)
            break
        except ValueError:
            print("Invalid input! Please enter a valid number! ")
    return number


def determine_user_choice(user_input, movies):
    """chooses what to do based on user input"""
    if user_input == "0":
        print("Bye!")
        sys.exit()

    possible_choices = {
        "1": list_movies,
        "2": add_movie,
        "3": delete_movie,
        "4": update_movie,
        "5": print_stats,
        "6": print_random_movie,
        "7": search_movie,
        "8": sort_by_rating,
        "9": sort_by_year,
        "10": filter_movies
    }
    possible_choices[user_input](movies)


if __name__ == "__main__":
    main()
