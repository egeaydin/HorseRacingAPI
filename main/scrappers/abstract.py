from bs4 import BeautifulSoup
import urllib.request
import datetime
from . import logger
from main.exception import PageDoesNotExist
import time
from main.enums import ManagerType
from main.models import Result


class BaseRaceDayScrapper:
    """
    Race Day Scrapper(RDS) makes a request to an url in order to get the page source that contains information about
    the past, present or upcoming races usually from Turkey.
    """

    """
    Each race day contains many races and each of them wrapped by a single div tag, and it's class is 'races-panes'.
    We store that div inside this property
    """
    race_divs = ''

    """
    Fixture and Result pages have minor differences, therefore they need different scrappers to scrap html table rows
    """
    row_scrapper = ''

    page_type = ''

    url = ''

    rows = list()

    """
        Fixture and Result has one particular difference in the url, thus this property determines that
        Fixture: 'GunlukYarisProgrami'
        Result: 'GunlukYarisSonuclari'
        """
    race_type = ''

    def __init__(self, city, date):
        self.race_day = ''
        self.city = city
        self.date = date

        self.set_url()

        try:
            # Get the html of the page that contains the results
            self.html = urllib.request.urlopen(self.url).read()
        except urllib.request.HTTPError as http_error:
            raise PageDoesNotExist(str(http_error), self.url)

        self.race_divs = self.get_race_divs()

    @classmethod
    def from_date_values(cls, city, year, month, day):
        return cls(city, datetime.date(year, month, day))

    def set_url(self):
        # -- start url parsing --
        # {0} is race type, {1} is city id, {2} is city name
        self.url = 'http://www.tjk.org/TR/YarisSever/Info/Sehir/{0}?SehirId={' \
                   '1}&QueryParameter_Tarih={2}&SehirAdi={3}'

        # Feeding the city information to url
        self.url = self.url.format(self.race_type, self.city.value, '{0}', self.city.name)

        # Feeding the date information to url by formatting the date to appropriate string
        # Ex: '03%2F07%2F2017'
        # But first we use dashes as separator so we won't confuse 'date.strftime' function
        date_format = '{0}-{1}-{2}'.format('%d', '%m', '%Y')

        # Now we are replacing dashes with appropriate chars to match the original url
        formatted_dated = self.date.strftime(date_format).replace('-', '%2F')

        self.url = self.url.format(formatted_dated)
        # -- end url parsing --

        logger.info(self.url)

    def get_race_divs(self):
        # Get the Soap object for easy scraping
        soup = BeautifulSoup(self.html, "lxml")

        # Get the div containing all the races
        race_div = soup.find("div", class_='races-panes')
        # Check if the page is valid
        if not race_div:
            raise PageDoesNotExist('', self.url)

        # Getting the one level inner divs which contains each race. Recursive is set to false because we don't want
        # to go the the inner child of those divs. Just trying to stay on the first level
        return race_div.find_all("div", recursive=False)

    def get(self):
        # Create an empty list to hold each race
        races = []
        # Process each race
        logger.info('Processing each race')

        for race_index, rDiv in enumerate(self.race_divs):
            logger.info('{0} race(s) remain'.format(len(self.race_divs) - race_index))

            # Get the raw race details
            race_id = int(rDiv.get('id'))

            race_detail_div = rDiv.find("div", class_="race-details")

            # The race_detail_div contains some needed information on one of it's children <h3>
            race_info_html = race_detail_div.find("h3", class_="race-config")

            # After the first 'a' tag we have a text that has the info we need
            race_info = race_info_html.find('a').next_sibling

            # We split from the comma and at the last element the we we get
            # Race_info: '   1100\r\n\r\nÇim'
            race_info = race_info.split(",")[-1]

            # Split to separate distance and track type
            race_info = race_info.split("\r\n\r\n")

            # distance is the first element and it has unnecessary space on it, we remove those
            distance = race_info[0].replace(" ", "")

            # track_type is the second element and it has unnecessary space and some characters on it, we remove those
            track_type = race_info[1].replace(" ", "").replace("\n", "").replace("\r", "")

            # Common data for the race is ready, time to get the results get the result of each horse in the table
            rows = rDiv.find("tbody").find_all("tr")

            # Create an empty list to hold each result for this race
            results = []
            # Go through the each result and process
            for i, row in enumerate(rows):
                # Initialize the scrapper for a single row
                scrapper = self.row_scrapper(row)

                # Get the result model with scrapped data in it
                model = scrapper.get()

                # Assign the values that are specific to this race
                model.track_type = track_type
                model.distance = int(distance)
                model.race_id = race_id
                model.city = self.city.name
                model.race_date = self.date

                # Append the model to the result list
                results.append(model)
            # This point we have all the results of one race we can append it to the race list
            races.append(results)

            self.rows.append(rows)
        # We got all the information about the race day in the given city and date. We can return the races list now
        logger.info('Completed!')
        return races

    @classmethod
    def scrap_by_date(cls, city, date):
        """
        Scraps the results of the supplied city and date
        :param city: City which the race happened
        :param date: datetime object for the desired race
        :return: Returns the results of the desired race
        """
        scrapper = cls(city, date)
        return scrapper.get()

    @classmethod
    def scrap(cls, city, year, month, day):
        """
        Scraps the results of the supplied city and date values
        :param city: City which the race happened
        :param year: The year of the wanted race
        :param month: The month of the wanted race
        :param day: The day of the wanted race
        :return: Returns the results of the desired race
        """
        return cls.scrap_by_date(city, datetime.datetime(year, month, day))


class BaseRaceDayRowScrapper:
    """
      Class name used for horses' name in TJK's site, after "gunluk-GunlukYarisProgrami-"
      Ex: <td class="gunluk-GunlukYarisProgrami-AtAdi">
      """
    horse_name_class_name = ''
    page_type = ''

    """
    Beginning of the class name used for each row in the tables, Fixture and Result tables has it differently
    Ex for fixture: <td class="gunluk-GunlukYarisProgrami-AtAdi">
    Ex for result: <td class="gunluk-GunlukYarisSonuclari-AtAdi3">
    """
    td_class_base = ''

    def __init__(self, html_row):
        self.row = html_row

    def get(self):
        model = Result()

        # Jockey, owner and trainer's have their id's just like the horse's own id. We are only interested in their
        # ids so we don't bother to get their names
        model.jockey_id = self.get_manager_id(ManagerType.Jockey)
        model.owner_id = self.get_manager_id(ManagerType.Owner)
        model.trainer_id = self.get_manager_id(ManagerType.Trainer)

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
