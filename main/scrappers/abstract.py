from bs4 import BeautifulSoup
import urllib.request
import datetime
from . import logger
from main.exception import PageDoesNotExist
import time


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

    def __init__(self, city, date, html='', url='', get_past_statistics=False):
        self.get_past_statics = get_past_statistics
        self.race_day = ''
        self.city = city
        self.date = date

        self.set_url()

        # Try many times, occasionally it might fail
        try_counter = 20
        while True:
            try:
                # Get the html of the page that contains the results
                self.html = urllib.request.urlopen(self.url).read()
                break
            except urllib.request.HTTPError:
                if try_counter != 0:
                    time.sleep(1)
                    try_counter -= 1
                    continue

        self.is_valid_page()

        self.race_divs = self.get_race_divs()

    @classmethod
    def from_date_values(cls, city, year, month, day):
        return cls(city, datetime.date(year, month, day))

    def is_valid_page(self):
        if len(self.html) is 0:
            raise PageDoesNotExist('Could not find the race! Please make sure race is available on TJK.org. Url: {'
                                   '0}'.format(self.url))

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
            pass

        # Getting the one level inner divs which contains each race. Recursive is set to false because we don't want
        # to go the the inner child of those divs. Just trying to stay on the first level
        return race_div.find_all("div", recursive=False)

    def get(self):
        # Create an empty list to hold each race
        races = []
        # Process each race
        logger.info('Processing each race')

        if self.get_past_statics:
            logger.info('{0} races|get_past_statics is on, going to take a moment to complete!'.format(
                len(self.race_divs)))

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

                if self.get_past_statics:
                    logger.info('{0} horse(s) remain'.format(len(rows) - i))
                    model.set_past_results()

                # Append the model to the result list
                results.append(model)
            # This point we have all the results of one race we can append it to the race list
            races.append(results)

            self.rows.append(rows)
        # We got all the information about the race day in the given city and date. We can return the races list now
        logger.info('Completed!')
        return races

    @classmethod
    def scrap_by_date(cls, city, date, get_past_statistics=False):
        """
        Scraps the results of the supplied city and date
        :param city: City which the race happened
        :param date: datetime object for the desired race
        :return: Returns the results of the desired race
        """
        scrapper = cls(city, date, get_past_statistics=get_past_statistics)
        return scrapper.get()

    @classmethod
    def scrap(cls, city, year, month, day, get_past_statistics=False):
        """
        Scraps the results of the supplied city and date values
        :param city: City which the race happened
        :param year: The year of the wanted race
        :param month: The month of the wanted race
        :param day: The day of the wanted race
        :return: Returns the results of the desired race
        """
        return cls.scrap_by_date(city, datetime.datetime(year, month, day), get_past_statistics)
