import random


class MovieApp:
    def __init__(self, storage):
        self._storage = storage


    def __print_header(self):
        """prints program header"""
        print("*" * 10 + " My Movies Database " + "*" * 10)


    def __display_menu(self):
        """printing menu"""
        print()
        print("Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
              "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
              "8. Movies sorted by rating\n9. Movies sorted by year\n10. Filter movies")
        print()


    def _command_list_movies(self):
        self._storage.list_movies()


    def _generate_website(self):
        ...


    def run(self):
        while True:
            self.__display_menu()
            user_choice = (input("Enter a number between 0 and 10: "))
            if user_choice == "0":
                print("Bye!")
                return
            try:
                self.__determine_user_choice(user_choice, self._storage.movies)
            except KeyError:
                print("Invalid option. Please choose a number between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")


    def __determine_user_choice(self, user_input, movies):
        """chooses what to do based on user input"""
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


    def __validate_input(self, data_type):
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


    def __command_print_stats(self):
        """calculating and printing average, median and lowest and highest ratings"""
        # summing up, dividing by length and printing average
        self._storage.print_stats()

    def __print_random_movie(self):
        """choosing and printing a random movie from the movies list"""
        random_movie = random.choice(movies)
        print(f"Your random movie for today is '{random_movie['title']}' "
              f"({random_movie['year']}) with a rating of {random_movie['rating']}")


    def __command_search_movie(self):
        """allows user to search movies using a part of the title"""
        user_search = input("Please type a part of the movie title! ").lower()
        self._storage.__search_movie(user_search)


    def __sort_by_year(self):
        """sorting our movies list ascending or descending depending on the user's choice"""
        print("Do you want the latest movies first? (Y/N)")
        while True:
            user_input = input("").lower()
            if user_input == "n":
                movies_sorted_by_year = sorted(self._storage.movies, key=lambda movie: movie["year"])
                break
            if user_input == "y":
                movies_sorted_by_year = sorted(self._storage.movies, key=lambda movie: movie["year"], reverse=True)
                break
            print("Invalid input. Enter 'Y' or 'N'! ")

        for mov in movies_sorted_by_year:
            print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


    def __sort_by_rating(self):
        """prints movies sorted by rating, descending"""
        movies_sorted_by_rating_descending = sorted(self._storage.movies,key=lambda movie: movie["rating"], reverse=True)
        for mov in movies_sorted_by_rating_descending:
            print(f"{mov['title']} ({mov['year']}): {mov['rating']}")


    def __filter_movies(self):
        """prints movies that fulfill conditions defined by user"""
        print("Enter minimum rating - leave blank for no minimum rating ")
        minimum_rating = self.__validate_input(float)

        print("Enter start year - leave blank for no start year! ")
        start_year = self.__validate_input(int)

        print("Enter end year - leave blank for no end year! ")
        end_year = self.__validate_input(int)

        # creating list of movies that fit the criteria defined by the user
        valid_movies = [movie for movie in self._storage.movies if (minimum_rating is None or movie["rating"] >= minimum_rating)
                        and (start_year is None or start_year <= movie["year"])
                        and (end_year is None or movie["year"] <= end_year)]

        for valid_movie in valid_movies:
            print(f"{valid_movie['title']} ({valid_movie['year']}): {valid_movie['rating']}")


    def __command_add_movie(self):
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


    def __command_delete_movie(self):
        """checks if chosen movie exists and, if yes, deletes it"""
        to_delete = input("Which movie would you like to delete? ").lower()
        self._storage.delete_movie(to_delete)


    def __command_update_movie(self):
        """allowing user to update movie rating if the desired movie exists in the list"""
        to_update = input("Which movie would you like to update? ").lower()
        # checking whether the desired movie exists and assigning it to mov, otherwise mov will be None
        mov = next((movie for movie in movies if movie["title"].lower() == to_update), None)

        if mov is None:
            # movie is called "mov" here because otherwise it shadowed a name
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




