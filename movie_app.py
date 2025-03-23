class MovieApp:
    def __init__(self, storage):
        self._storage = storage


    def run(self):
        while True:
            self.__display_menu()
            user_choice = (input("Enter a number between 0 and 10: "))
            if user_choice == "0":
                print("Bye!")
                return
            try:
                self.__determine_user_choice(user_choice)
            except KeyError:
                print("Invalid option. Please choose a number between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")


    def __determine_user_choice(self, user_input):
        """chooses what to do based on user input"""
        possible_choices = {
            "1": self.__command_list_movies,
            "2": self.__command_add_movie,
            "3": self.__command_delete_movie,
            "4": self.__command_update_movie,
            "5": self.__command_print_stats,
            "6": self.__command_print_random_movie,
            "7": self.__command_search_movie,
            "8": self.__command_sort_by_rating,
            "9": self.__command_sort_by_year,
            "10": self.__command_filter_movies
        }
        possible_choices[user_input]()


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


    def __command_list_movies(self):
        self._storage.list_movies()


    def __command_add_movie(self):
        """allows user to add a movie with release year and rating"""
        title = input("Please enter the movie name! ")
        poster = input("Please enter the poster name!")

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
        self._storage.add_movie(title, year, rating, poster)


    def __command_delete_movie(self):
        """checks if chosen movie exists and, if yes, deletes it"""
        to_delete = input("Which movie would you like to delete? ").lower()
        self._storage.delete_movie(to_delete)


    def __command_update_movie(self):
        """allowing user to update movie rating if the desired movie exists in the list"""
        title = input("Which movie would you like to update? ").lower()

        while True:
            print("Please enter a new rating! ")
            try:
                new_rating = float(input(""))
                self._storage.update_movie(title, new_rating)
                break
            except ValueError:
                print("Invalid rating! ")


    def __command_print_stats(self):
        """calculating and printing average, median and lowest and highest ratings"""
        # summing up, dividing by length and printing average
        self._storage.print_stats()


    def __command_print_random_movie(self):
        """choosing and printing a random movie from the movies list"""
        self._storage.print_random_movie()


    def __command_search_movie(self):
        """allows user to search movies using a part of the title"""
        user_search = input("Please type a part of the movie title! ").lower()
        self._storage.search_movie(user_search)


    def __command_sort_by_rating(self):
        """prints movies sorted by rating, descending"""
        self._storage.sort_by_rating()


    def __command_sort_by_year(self):
        """sorting our movies list ascending or descending depending on the user's choice"""
        print("Do you want the latest movies first? (Y/N)")
        while True:
            user_input = input("").lower()
            if user_input != "y" and user_input != "n":
                print("Invalid input. Enter 'Y' or 'N'! ")
            else:
                self._storage.sort_by_year(user_input)
                break


    def __command_filter_movies(self):
        """prints movies that fulfill conditions defined by user"""
        print("Enter minimum rating - leave blank for no minimum rating ")
        minimum_rating = self.__validate_input(float)

        print("Enter start year - leave blank for no start year! ")
        start_year = self.__validate_input(int)

        print("Enter end year - leave blank for no end year! ")
        end_year = self.__validate_input(int)

        self._storage.filter_movies(minimum_rating, start_year, end_year)


    def _generate_website(self):
        ...
