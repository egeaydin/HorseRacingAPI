# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server

from main.enums import PageType
from .abstract import BaseRaceDayRowScrapper


class FixtureRowScrapper(BaseRaceDayRowScrapper):
    """
    Ex: <td class="gunluk-GunlukYarisProgrami-AtAdi">
    """
    horse_name_class_name = "AtAdi"
    td_class_base = 'gunluk-GunlukYarisProgrami-'
    page_type = PageType.Fixture

    def get(self):
        fixture = super(FixtureRowScrapper, self).get()

        fixture.order = int(self.get_column_content('SiraId'))

        return fixture


class ResultRowScrapper(BaseRaceDayRowScrapper):
    """
    Ex: <td class="gunluk-GunlukYarisProgrami-AtAdi3">
    """
    horse_name_class_name = "AtAdi3"
    td_class_base = 'gunluk-GunlukYarisSonuclari-'
    page_type = PageType.Result

    def get(self):
        result = super(ResultRowScrapper, self).get()

        # Horses name still has the order that horse started the race in the first place.
        # Example "KARAHİNDİBAYA (7)"
        horse_name_and_order = result.horse_name.split("(")

        result.horse_name = str(horse_name_and_order[0])

        # Example after split: "7)"
        result.order = int(horse_name_and_order[1].replace(')', ''))

        # Get the result of the horse from the second column
        result.result = self.get_column_content("SONUCNO")

        # Horses sometimes may not run
        # Horses might not run that race or cannot finish it for various reasons. In that case what we get is an
        # empty string, we mark it as -1 if that happens
        if not result.result:
            result.result = -1
        else:
            result.result = int(result.result)

        # Get the time that it took horse to run this race
        result.time = self.get_column_content("Derece")
        # Hc and Hk are two different handicap types that is possible
        result.handicap = int(self.get_column_content("Hc") or self.get_column_content("Hk"))
        return result

