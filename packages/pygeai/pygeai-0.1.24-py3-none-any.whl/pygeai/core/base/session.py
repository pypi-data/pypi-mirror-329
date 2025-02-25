import os
import sys

from pygeai.core.common.config import get_settings
from pygeai.core.common.exceptions import MissingRequirementException
from pygeai.core.singleton import Singleton

settings = get_settings()


# TODO -> Review if it's convenient to use singleton over precise parameters
class Session(metaclass=Singleton):
    """
    A session to store configuration state required to interact with different resources.

    Args:
        api_key (str): Key to interact with API of GEAI
        base_url (str): Base URL to connect to instance of GEAI

    Returns:
        Instance of Session
    """

    def __init__(
            self,
            api_key: str,
            base_url: str
        ):
        self.__api_key = api_key
        self.__base_url = base_url

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str):
        self.__api_key = api_key

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self.__base_url = base_url


def get_session(alias: str = "default") -> Session:
    """
    Session is a singleton object:
    On the first invocation, returns Session configured with the API KEY and BASE URL corresponding to the
    alias provided. On the following invocations, it returns the first object instantiated.
    """
    try:
        return Session(
            api_key=settings.get_api_key(alias),
            base_url=settings.get_base_url(alias)
        )
    except ValueError as e:
        sys.stdout.write("Warning: API_KEY and/or BASE_URL not set. Please run geai configure to set them up.\n")
