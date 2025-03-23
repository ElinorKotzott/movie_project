from app import App


class MovieApp:
    def __init__(self, storage):
        self._storage = storage


    def run(self):
        """starts application loop, printing header and menu, getting user input for
        the menu and sending user choice in to be processed"""
        self.__print_header()
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
            "10": self.__command_generate_website
        }
        possible_choices[user_input]()


    def __validate_input(self, data_type):
        """validates user input and returns it"""
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
              "8. Movies sorted by rating\n9. Movies sorted by year\n10. Generate website")
        print()


    def __command_list_movies(self):
        """calls list_movies on an instance of iStorage"""
        self._storage.list_movies()


    def __command_add_movie(self):
        """asks for user input and calls add_movie on an instance of iStorage"""
        title = input("Please enter the movie name! ")
        self._storage.add_movie(title)


    def __command_delete_movie(self):
        """asks for user input and calls delete_movie on an instance of iStorage"""
        to_delete = input("Which movie would you like to delete? ").lower()
        self._storage.delete_movie(to_delete)


    def __command_update_movie(self):
        """asks for user_input for title and new rating, sending both into the call
        of update_movie on an instance of iStorage"""
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
        """calls print_stats on an instance of iStorage"""
        self._storage.print_stats()


    def __command_print_random_movie(self):
        """calls print_random_movie on an instance of iStorage"""
        self._storage.print_random_movie()


    def __command_search_movie(self):
        """gets user input and calls search_movie on an instance of iStorage"""
        user_search = input("Please type a part of the movie title! ").lower()
        self._storage.search_movie(user_search)


    def __command_sort_by_rating(self):
        """calls sort_by_rating on an instance of iStorage"""
        self._storage.sort_by_rating()


    def __command_sort_by_year(self):
        """gets user_input and calls sort_by_year on an instance of iStorage"""
        print("Do you want the latest movies first? (Y/N)")
        while True:
            user_input = input("").lower()
            if user_input != "y" and user_input != "n":
                print("Invalid input. Enter 'Y' or 'N'! ")
            else:
                self._storage.sort_by_year(user_input)
                break


    def __command_generate_website(self):
        """creates an instance of the App class and calls create_website on it, sending in the movies
        returned by list_movies"""
        my_app = App()
        my_app.create_website(self._storage.list_movies())
