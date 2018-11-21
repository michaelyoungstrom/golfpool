from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Tournament

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.last_name + ',' + self.first_name

class PlayerEvent(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    pool = models.IntegerField()
    round_one_to_par = models.IntegerField(blank=True)
    round_two_to_par = models.IntegerField(blank=True)
    round_three_to_par = models.IntegerField(blank=True)
    round_four_to_par = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.tournament) + ' ' + str(self.player)

class UserEvent(models.Model):
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)
    player_events = models.ManyToManyField(PlayerEvent)
    total_score_to_par = models.IntegerField(default=0)
