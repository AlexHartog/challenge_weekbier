from enum import Enum
from datetime import timedelta

from django.db import models


class Player(models.Model):
    """A player participating in the challenge."""
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    _score = None
    _valid_checkins = None
    _score_checkins = None

    def num_checkins(self):
        return len(self.get_valid_checkins())

    def num_weeks_scored(self):
        week_numbers = set()

        for checkin in self.get_valid_checkins():
            # Add one day to start the new week on Sunday
            week_numbers.add((checkin.date + timedelta(days=1)).isocalendar()[1])

        return len(week_numbers)

    def get_valid_checkins(self):
        if self._valid_checkins is None:
            self._valid_checkins = [checkin for checkin in self.checkin_set.all() if checkin.is_valid()]

        return self._valid_checkins

    def get_score_checkins(self):
        if self._score_checkins is None:
            self._score_checkins = [checkin for checkin in self.checkin_set.all() if checkin.gives_points()]

        return self._score_checkins

    def score(self):
        if self._score is None:
            self._score = self.num_weeks_scored() * 2 + len(self.get_score_checkins())

        return self._score

    def __str__(self):
        """Return a string representation of the model."""
        return self.name


class Checkin(models.Model):
    """A checkin for a player."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    place = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    cached_status = None

    def status(self):
        if Checkin.objects.filter(player=self.player, date__lt=self.date, city=self.city).count() > 0:
            return self.Status.DUPLICATE_CITY
        elif Checkin.objects.filter(player=self.player, date=self.date, date_added__lt=self.date_added).count() > 0:
            return self.Status.DUPLICATE_CHECKIN_ON_DATE
        elif (self.date + timedelta(days=1)).isocalendar()[1] == 1 and \
                Checkin.objects.filter(player=self.player, date__lt=self.date).count() > 0:
            return self.Status.DUPLICATE_FIRST_WEEK
        else:
            return self.Status.OK

    def is_valid(self):
        return self.status() in [self.Status.OK, self.Status.DUPLICATE_FIRST_WEEK]

    def gives_points(self):
        return self.status() == self.Status.OK

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.player.name} checked in for {self.date} at {self.place} in {self.city} at {self.date_added}"

    class Status(Enum):
        OK = ""
        DUPLICATE_CITY = "Dubbele stad"
        DUPLICATE_CHECKIN_ON_DATE = "Dubbele checkin op datum"
        DUPLICATE_FIRST_WEEK = "Dubbele checkin in eerste week"
