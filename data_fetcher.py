import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

url = f"http://www.omdbapi.com/?apikey={API_KEY}"


def get_movie_info_by_title(title):
    try:
        return requests.get(url + "&t=" + title).json()
    except requests.exceptions.ConnectionError:
        print("We cannot connect to the API. Please check your internet connection or try again later!")

