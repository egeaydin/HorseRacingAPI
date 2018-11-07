from django.db import models
from ..exception import MissingData
import time


class ResultMixin(models.Model):
    class Meta:
        abstract = True

    result = models.IntegerField(default=-1)
    handicap = models.IntegerField(default=-1)
    time = models.CharField(max_length=200, default=-1)

    @property
    def time_as_seconds(self):
        """
            Returns the time string obtanied from the TJK web site to seconds, since split-secods are involved for
            this use case, our seconds are going to be floats
        :return:
        """
        # 1.30.54 or 59.32

        # 100 split-second = 1 second
        # 1 minute = 60 seconds
        units_as_seconds = [0.01, 1, 60]

        # Split by the dot
        split = self.time.split('.')

        if self.time == "Derecesiz":
            raise MissingData('Horse either did not finish the race, or had not run in the first place!')

        # Reverse the array to start from the split-second since minutes might not be there
        reversed_time = split[::-1]

        total_seconds = 0
        # Multiply the value by corresponding unit value and add it to total_seconds
        for i, t in enumerate(reversed_time):
            total_seconds += int(t) * units_as_seconds[i]
        return round(total_seconds, 2)
