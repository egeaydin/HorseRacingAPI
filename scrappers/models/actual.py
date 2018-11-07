from .abstract import BasePage, BaseRaceDay
from .mixin import ResultMixin


class Result(BaseRaceDay, ResultMixin):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Result:" + super(Result, self).__str__()


class Fixture(BaseRaceDay):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Fixture:" + super(Fixture, self).__str__()


class Horse(BasePage, ResultMixin):
    class Meta:
        app_label = 'horsing_around'

    def __str__(self):
        return "Horse Result:" + super(Horse, self).__str__()
