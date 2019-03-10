from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Tournament

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.last_name + ', ' + self.first_name

class PlayerEvent(models.Model):
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)
    total_score_to_par = models.IntegerField(blank=True, null=True)
    todays_score_to_par = models.IntegerField(blank=True, null=True)
    holes_played_today = models.IntegerField(blank=True, null=True)
    round_one_total_score = models.IntegerField(blank=True, null=True)
    round_two_total_score = models.IntegerField(blank=True, null=True)
    round_three_total_score = models.IntegerField(blank=True, null=True)
    round_four_total_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.tournament) + ' ' + str(self.player)

class Pool(models.Model):
    pool_id = models.CharField(max_length=1)
    tournament = models.ForeignKey(Tournament)
    players = models.ManyToManyField(Player)

    @property
    def sorted_players(self):
        return self.players.order_by('last_name')

class UserEvent(models.Model):
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)
    position = models.IntegerField(blank=True, null=True)
    players = models.ManyToManyField(Player)
    round_one_to_par = models.IntegerField(default=0)
    round_two_to_par = models.IntegerField(default=0)
    round_three_to_par = models.IntegerField(default=0)
    round_four_to_par = models.IntegerField(default=0)
    total_score_to_par = models.IntegerField(default=0)
