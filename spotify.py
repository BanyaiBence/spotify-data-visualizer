import json
from enum import Enum
import requests
import random

class SearchType(Enum):
    """Enum to represent the different types of items that can be searched for on Spotify

    Args:
        Enum (str): The type of item that can be searched for on Spotify
    """
    ALBUM = "album"
    ARTIST = "artist"
    TRACK = "track"
    YEAR = "year"
    UPC = "upc"
    ISRC = "isrc"
    GENRE = "genre"

class Endpoint(Enum):
    """Enum to represent the different endpoints of the Spotify API

    Args:
        Enum (str): The endpoint of the Spotify API
    """
    ALBUMS = "albums"
    ARTISTS = "artists"
    SEARCH = "search"
    FOLLOW = "follow"
    LIBRARY = "library"
    ME = "me"

class Spotify():
    """Class to interact with the Spotify API

    Returns:
        Spotify: The Spotify object
    """
    URL = "https://api.spotify.com/v1/"
    def __init__(self):
        super().__init__()
        self.token = self._get_token()

        for search_type in SearchType:
            setattr(self, f"search_{search_type.value}", self._create_search_func(search_type))

    def search_artist(self, *args, **kwargs) -> dict:
        return {}
    def search_album(self, *args, **kwargs) -> dict:
        return {}
    def search_track(self, *args, **kwargs) -> dict:
        return {}
    def search_year(self, *args, **kwargs) -> dict:
        return {}
    def search_upc(self, *args, **kwargs) -> dict:
        return {}
    def search_isrc(self, *args, **kwargs) -> dict:
        return {}
    def search_genre(self, *args, **kwargs) -> dict:
        return {}

    def _get_data(self, endpoint: str, timeout: int = 5) -> dict:
        """ Retrieve data from Spotify API

        Args:
            endpoint (str): The endpoint to retrieve data from
            token (str): The token to authenticate the request
            timeout (int, optional): The timeout for the request. Defaults to 5.

        Returns:
            dict: The json response from the request
        """
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(endpoint, headers=headers, timeout=timeout)
        return response.json()
    
    def _get_token(self, timeout: int = 5) -> str:
        """This function gets the token from the Spotify API

        Args:
            timeout (int, optional): The time in seconds to wait for the response. Defaults to 5.

        Returns:
            str: The token to be used in the API requests
        """
        with open("secrets.json", 'r', encoding="UTF-8") as f:
            try:
                secrets = json.load(f)
            except FileNotFoundError:
                print("Secrets file not found")
                exit()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': secrets['client_id'],
            'client_secret': secrets['client_secret']
        }

        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data, timeout=timeout)    

        if response.status_code != 200:
            print(response.status_code)
            print(response.json())
            exit()
        

        return response.json()['access_token']

    def get_artist(self, artist_id: str) -> dict:
        """ Retrieve data about an artist

        Args:
            artist_id (str): The artist's ID
            token (str): The token to authenticate the request

        Returns:
            dict: The json response from the request
        """
        endpoint = f"{Spotify.URL + Endpoint.ARTISTS.value}/{artist_id}"
        return self._get_data(endpoint)

    def _search(self, query: str, search_type: SearchType, limit: int=10, offset: int = 0) -> dict:
        """ Search for an item

        Args:
            query (str): The query to search for
            type (SearchType): The type of item to search for
            limit (int, optional): The number of items to return. Defaults to 10.
            offset (int, optional): The index of the first item to return. Defaults to 0.
            token (str, optional): The token to authenticate the request. Defaults to None.

        Returns:
            dict: The json response from the request
        """
        endpoint = f"{Spotify.URL
        + Endpoint.SEARCH.value}?q={query}&type={search_type.value}&limit={limit}&offset={offset}"
        return self._get_data(endpoint)

    def _create_search_func(self, search_type: SearchType):
        def search_func(query: str, limit: int=10, offset: int = 0) -> dict:
            return self._search(query, search_type, limit, offset)
        return search_func
    
    def get_albums_of_artist(self, artist_id: str) -> dict:
        """ Retrieve the albums of an artist

        Args:
            artist_id (str): The artist's ID
            token (str): The token to authenticate the request

        Returns:
            dict: The json response from the request
        """
        endpoint = f"{Spotify.URL + Endpoint.ARTISTS.value}/{artist_id}/albums"
        return self._get_data(endpoint)

    def get_album(self, album_id: str) -> dict:
        """ Retrieve data about an album

        Args:
            album_id (str): The album's ID
            token (str): The token to authenticate the request

        Returns:
            dict: The json response from the request
        """
        endpoint = f"{Spotify.URL + Endpoint.ALBUMS.value}/{album_id}"
        return self._get_data(endpoint)
