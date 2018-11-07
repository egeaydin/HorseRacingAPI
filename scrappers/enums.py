from enum import Enum
import importlib


class PageType(Enum):
    """
    Cities and their are respected ids determined by TJK.org for their query parameters
    """
    Fixture = 'F'
    Result = 'R'
    Horse = 'H'

    @property
    def scrapper(self):
        scrapper_module = importlib.import_module("scrappers.page")
        return getattr(scrapper_module, '{0}Scrapper'.format(self.name))

    @property
    def model(self):
        model_module = importlib.import_module("scrappers.models")
        return getattr(model_module, self.name)


class City(Enum):
    """
    Cities and their are respected ids determined by TJK.org for their query parameters
    """
    Izmir = 2
    Istanbul = 3
    Bursa = 4
    Adana = 1
    Ankara = 5
    Kocaeli = 9
    Urfa = 6
    Elazig = 7
    Diyarbakir = 8


class ManagerType(Enum):
    """
    The class of the columns in the each race table
    """
    Jockey = 'JokeAdi'
    Owner = 'SahipAdi'
    Trainer = 'AntronorAdi'