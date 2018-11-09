from django import forms
from datetime import datetime


class RaceDayURLQueryForm(forms.Form):
    """
    Django forms are great way to validate the given parameters to the URL.
    The purpose of this class is to validate the url for getting race day data
    """
    year = forms.IntegerField(max_value=9999, min_value=1000, required=True)
    month = forms.IntegerField(max_value=12, min_value=1, required=True)
    day = forms.IntegerField(max_value=31, min_value=1, required=True)

    @property
    def race_date(self):
        if self.is_valid():
            return datetime(self.cleaned_data['year'],
                            self.cleaned_data['month'],
                            self.cleaned_data['day'])
