# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server

from .row import FixtureRowScrapper, ResultRowScrapper
from main.enums import PageType
from .abstract import BaseRaceDayScrapper


class FixtureScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisProgrami'
    row_scrapper = FixtureRowScrapper
    page_type = PageType.Fixture


class ResultScrapper(BaseRaceDayScrapper):
    """
    Ex: 'http://www.tjk.org/EN/YarisSever/Info/Sehir/GunlukYarisSonuclari?SehirId=9&QueryParameter_Tarih=26%2F09%2F2017&SehirAdi=Kocaeli'
    """
    race_type = 'GunlukYarisSonuclari'
    row_scrapper = ResultRowScrapper
    page_type = PageType.Result
