from datetime import timedelta
from enum import Enum

from django.db import models


class Player(models.Model):
    FIRST_WEEK_CUTOFF = "2023-01-08"

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
            distinct_city_checkins = self.checkin_set.order_by(
                "player", "city", "date"
            ).distinct("player", "city")
            distinct_date_checkins = distinct_city_checkins.order_by(
                "player", "date", "date_added"
            ).distinct("player", "date")
            self._valid_checkins = distinct_date_checkins

        return self._valid_checkins

    def get_score_checkins(self):
        if self._score_checkins is None:
            first_week_checkin = self._valid_checkins.filter(
                date__lt=self.FIRST_WEEK_CUTOFF
            ).distinct("player")
            other_checkins = self._valid_checkins.filter(
                date__gte=self.FIRST_WEEK_CUTOFF
            )
            self._score_checkins = first_week_checkin.union(other_checkins)

        return self._score_checkins

    def score(self):
        if self._score is None:
            self._score = self.num_weeks_scored() * 2 + len(self.get_score_checkins())

        return self._score

    def __str__(self):
        """Return a string representation of the model."""
        return self.name


class CheckinManager(models.Manager):
    def ordered_by_date(self):
        return self.order_by("-date")

    def filtered(self, player_id=None, player=None, place=None, city=None):
        filtered_checkins = self.ordered_by_date()
        if player_id:
            filtered_checkins = filtered_checkins.filter(player=player_id)
        if player:
            filtered_checkins = filtered_checkins.filter(player__name__icontains=player)
        if place:
            filtered_checkins = filtered_checkins.filter(place__icontains=place)
        if city:
            filtered_checkins = filtered_checkins.filter(city__icontains=city)
        return filtered_checkins

    def filter_exact(self, player_id=None, player=None, place=None, city=None):
        filtered_checkins = self.ordered_by_date()
        if player_id:
            filtered_checkins = filtered_checkins.filter(player=player_id)
        if player:
            filtered_checkins = filtered_checkins.filter(player__name__iexact=player)
        if place:
            filtered_checkins = filtered_checkins.filter(place__iexact=place)
        if city:
            filtered_checkins = filtered_checkins.filter(city__iexact=city)
        return filtered_checkins


class Checkin(models.Model):
    """A checkin for a player."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    place = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    cached_status = None

    objects = CheckinManager()

    def status(self):
        if (
            Checkin.objects.filter(
                player=self.player, date__lt=self.date, city=self.city
            ).count()
            > 0
        ):
            return self.Status.DUPLICATE_CITY
        elif (
            Checkin.objects.filter(
                player=self.player, date=self.date, date_added__lt=self.date_added
            ).count()
            > 0
        ):
            return self.Status.DUPLICATE_CHECKIN_ON_DATE
        elif (self.date + timedelta(days=1)).isocalendar()[
            1
        ] == 1 and Checkin.objects.filter(
            player=self.player, date__lt=self.date
        ).count() > 0:
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
