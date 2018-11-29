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
    round_one_to_par = models.IntegerField(default=0, blank=True, null=True)
    round_two_to_par = models.IntegerField(default=0, blank=True, null=True)
    round_three_to_par = models.IntegerField(default=0, blank=True, null=True)
    round_four_to_par = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.tournament) + ' ' + str(self.player)

class UserEvent(models.Model):
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)
    position = models.IntegerField(blank=True, null=True)
    player_events = models.ManyToManyField(PlayerEvent)
    round_one_to_par = models.IntegerField(default=0)
    round_two_to_par = models.IntegerField(default=0)
    round_three_to_par = models.IntegerField(default=0)
    round_four_to_par = models.IntegerField(default=0)
    total_score_to_par = models.IntegerField(default=0)
