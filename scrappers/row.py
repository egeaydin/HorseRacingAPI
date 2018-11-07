# -*- coding: utf-8 -*-
# The above line is for turkish characters in comments, unless it is there a encoding error is raised in the server
from .enums import ManagerType, PageType
from . import logger
import datetime


class BaseRowScrapper:
    test_model = ''
    page_type = ''

    def __init__(self, html_row):
        self.row = html_row

    def get(self):
        model = self.page_type.model()

        # Jockey, owner and trainer's have their id's just like the horse's own id. We are only interested in their
        # ids so we don't bother to get their names
        model.jockey_id = self.get_manager_id(ManagerType.Jockey)
        model.owner_id = self.get_manager_id(ManagerType.Owner)
        model.trainer_id = self.get_manager_id(ManagerType.Trainer)

        return model

    def get_manager_id(self, _type):
        """
        :param _type: The content of the column where the according type of manager is
        :return: id of the desired manager either Jockey, Owner or Trainer
        """
        pass

    @staticmethod
    def get_id_from_a(a):
        """"
        The url's contain the id, after the phrase Id=
        :param a: The html code of a tag
        :return: id of the supplied a tag
        """
        if a:
            # We split from that and take the rest
            id_ = a['href'].split("Id=")[1]

            # We split one more time in case of there is more after the id
            # We take the first part this time
            id_ = id_.split("&")[0]

            return id_


class BaseRaceDayRowScrapper(BaseRowScrapper):
    """
      Class name used for horses' name in TJK's site, after "gunluk-GunlukYarisProgrami-"
      Ex: <td class="gunluk-GunlukYarisProgrami-AtAdi">
      """
    horse_name_class_name = ''

    """
    Beginning of the class name used for each row in the tables, Fixture and Result tables has it differently
    Ex for fixture: <td class="gunluk-GunlukYarisProgrami-AtAdi">
    Ex for result: <td class="gunluk-GunlukYarisSonuclari-AtAdi3">
    """
    td_class_base = ''

    def get(self):
        model = super(BaseRaceDayRowScrapper, self).get()
        # The third column in the table contains the name of the horse and a link that goes to that horse's page.
        # Also the link will have the id of the horse and the abbreviations that come after the name which tells
        # status information, for example whether the horse will run with an eye patch and etc.
        # More info is here: http://www.tjk.org/TR/YarisSever/Static/Page/Kisaltmalar
        horse_name_html = self.get_column(self.horse_name_class_name).find('a')

        # first element is the name it self, others are the abbreviations, so we get the first and assign it as name
        model.horse_name = str(horse_name_html.contents[0]).replace(" ", '')

        # Now get the id of the horse from that url
        model.horse_id = int(self.get_id_from_a(horse_name_html))

        # Get the model of the horse from the fourth column
        model.horse_age = self.get_column_content("Yas")

        # Horses father and mother are combined in a single column in separate <a> So we find all the <a> in the
        # column and only get their id's from respected links. Father is the first, mother is the second
        parent_links = self.get_column("Baba").find_all('a', href=True)

        # Process the father
        model.horse_father_id = int(self.get_id_from_a(parent_links[0]))

        # Process the mother
        model.horse_mother_id = int(self.get_id_from_a(parent_links[1]))

        # Get the weight of the horse during the time of the race
        model.horse_weight = self.get_column_content("Kilo")

        return model

    def get_manager_id(self, _type):
        """
        :param _type: The content of the column where the according type of manager is
        :return: id of the desired manager either Jockey, Owner or Trainer
        """
        try:
            # Sometimes the info is not there, so we have to be safe
            return int(self.get_id_from_a(self.get_column(_type.value).find('a', href=True)))
        except:
            # Info is not there, mark it as missing
            return -1

    def get_column(self, col_name):
        """
        :param col_name: The value after the gunluk-GunlukYarisSonuclari-{0}
        :return: The content in the column(td) that has a class name starting with gunluk-GunlukYarisSonuclari-
        """
        return self.row.find("td", class_="{0}{1}".format(self.td_class_base, col_name))

    def get_column_content(self, col_name):
        """
        Striped_strings property returns a collection containing the values. Then ve do a string join to have the
        actual value in the tag. The value might me missing, then we simply return -1 to indicate that it is missing.
        :param col_name: The value after the gunluk-GunlukYarisSonuclari-{0}
        :return: The content in the column(td) that has a class name starting with gunluk-GunlukYarisSonuclari-
        """
        column = self.get_column(col_name)
        return "".join(column.stripped_strings if column else '-1')


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


class HorseRowScrapper(BaseRowScrapper):
    page_type = PageType.Horse

    def __init__(self, html_row):
        super(HorseRowScrapper, self).__init__(html_row)
        # Most of the columns do not have classes, we get all columns and assign each by hard-coding indexes
        self.columns = self.row.find_all("td")

    def get(self):
        model = super(HorseRowScrapper, self).get()

        date_and_race_id = self.columns[0]

        model.race_date = datetime.datetime.strptime(date_and_race_id.text, '\n%d.%m.%Y ')

        try:
            race_url = date_and_race_id.find('a', href=True)['href']
            # Race id is after the only hash-tag
            # Ex: /TR/YarisSever/Info/Page/GunlukYarisSonuclari?QueryParameter_Tarih=04/08/2017#111471
            # Split by hash-tag and get the second
            model.race_id = race_url.split('#')[1]
        except TypeError:
            # Some results don't have the races linked to them, so we mark it as missing
            model.race_id = -1

        model.city = str(self.get_column(1))
        model.distance = self.get_column(2)
        model.track_type = str(self.get_column(3))
        model.result = self.get_column(4)
        model.time = str(self.get_column(5))
        model.horse_weight = str(self.get_column(6))
        model.handicap = self.get_column(14)

        return model

    def get_manager_id(self, _type):
        """
        :param _type: The content of the column where the according type of manager is
        :return: id of the desired manager either Jockey, Owner or Trainer
        """
        index = 0
        if _type is ManagerType.Jockey:
            index = 7
        elif _type is ManagerType.Trainer:
            index = 12
        elif _type is ManagerType.Owner:
            index = 13
        else:
            raise Exception("Manager type not recognized!")

        try:
            return self.get_id_from_a(self.columns[index].find('a', href=True))
        except:
            raise Exception(self.row)

    def get_column(self, index):
        column = self.columns[index].stripped_strings
        for col in column:
            return col
        return -1
