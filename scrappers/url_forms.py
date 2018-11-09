from django import forms
from datetime import datetime
from .enums import City
from django.core.exceptions import ValidationError


class RaceDayURLQueryForm(forms.Form):
    """
    Django forms are great way to validate the given parameters to the URL.
    The purpose of this class is to validate the url for getting race day data
    """
    year = forms.IntegerField(max_value=9999, min_value=1000, required=True)
    month = forms.IntegerField(max_value=12, min_value=1, required=True)
    day = forms.IntegerField(max_value=31, min_value=1, required=True)
    city = forms.CharField(max_length=20, required=False)

    @property
    def race_date(self):
        if self.is_valid():
            return datetime(self.cleaned_data['year'],
                            self.cleaned_data['month'],
                            self.cleaned_data['day'])

    def clean_city(self):
        """
        City can be either ID or the actual name of the city we can easily validate it by trying to convert the value
        to enum's value or name. If enum is successfully generated then city is valid.
        :return:
        """
        city = self.cleaned_data['city']

        if city:
            # first check if incoming parameter is id
            try:
                city = City(int(city))
            except ValueError:
                # it is not id, now we check for the actual name
                # we are going to try to create the enum from the key
                try:
                    city = City[city]
                except KeyError:
                    # it is neither a valid id or a key, so we raise an error
                    raise ValidationError("Invalid value for City, City should be either valid city id or key",
                                          code='invalid')
            return city
