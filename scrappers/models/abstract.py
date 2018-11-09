from django.db import models
from ..util.collections import OrderedClassMembers
import copy
from ..page import HorseScrapper
from ..exception import PageDoesNotExist


class BasePage(models.Model):
    class Meta:
        abstract = True

    __metaclass__ = OrderedClassMembers
    race_id = models.IntegerField(default=0)
    race_date = models.DateTimeField(blank=True, null=True)
    horse_id = models.IntegerField()
    jockey_id = models.IntegerField()
    owner_id = models.IntegerField()
    trainer_id = models.IntegerField()
    horse_weight = models.CharField(max_length=200)
    track_type = models.CharField(max_length=200)
    distance = models.IntegerField()
    city = models.CharField(max_length=200)
    horse_name = models.CharField(max_length=200)
    horse_age = models.CharField(max_length=200)
    horse_father_id = models.IntegerField(default=-1)
    horse_mother_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=-1)

    def get_pure_dict(self, *remove_keys):
        # We need to have a separate dictionary because we are going to pop keys and we need to avoid changing the
        # original object
        ignore_keys = ['_state', 'html_row'] + list(remove_keys)

        filtered_dict = dict((k, v) for k, v in self.__dict__.items() if k not in ignore_keys)

        return filtered_dict

    def __str__(self):
        return "|".join(k + ': ' + repr(str(v)) for k, v in self.get_pure_dict('id').items())

    def __eq__(self, other):
        return self.get_pure_dict() == other.get_pure_dict()


class BaseRaceDay(BasePage):
    class Meta:
        abstract = True

    past_results = list()

    def set_past_results(self):
        past_scrapper = HorseScrapper(self.horse_id)
        try:
            self.past_results = past_scrapper.get()
        except PageDoesNotExist:
            pass

