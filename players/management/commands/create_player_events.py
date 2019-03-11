import click
import csv

from django.core.management.base import BaseCommand
from players.models import Player, PlayerEvent, UserEvent
from tournaments.models import Tournament

"""
Parses a csv file to add players to player events for a tournament.

Assumes a csv file with the following format (one line):
    tournament name, tournament year, player first name, player last name, pool number,
    round one score (optional), round two score (optional), round 3 score (optional), round 4 score (optional)

Additionally, this file will update additional values in the csv row if you choose to add score for each round
"""
class Command(BaseCommand):
    help = 'Adds player events to database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help="Relative path to csv file containing player event data")

    def get_relative_score(self, total_score, par):
        """
        Takes in a total score for a round and returns its relative score to par.
        """
        try:
            total_score_int = int(total_score)
        except:
            # Round isn't complete yet or they missed a cut/withdrew/etc
            return None

        return total_score_int - par

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file) as csv_file_object:
            csv_reader = csv.reader(csv_file_object, delimiter=',')
            for row in csv_reader:
                tournament_id = row[0]
                player_id = row[1]
                total_score_to_par = row[2]
                todays_score_to_par = row[3]
                holes_played_today = row[4]
                round_one_total_score = row[5]
                round_two_total_score = row[6]
                round_three_total_score = row[7]
                round_four_total_score = row[8]

                try:
                    tournament = Tournament.objects.get(tournament_id=tournament_id)
                except Tournament.DoesNotExist:
                    raise ValueError(
                        "Tournament with id: {} not found.".format(tournament_id)
                    )

                try:
                    player = Player.objects.get(player_id=player_id)
                except Player.DoesNotExist:
                    raise ValueError(
                        "Player with id: {} not found.".format(player_id)
                    )

                try:
                    player_event = PlayerEvent.objects.get(
                        tournament=tournament,
                        player=player
                    )
                except PlayerEvent.DoesNotExist:
                    player_event = PlayerEvent(
                        tournament=tournament,
                        player=player
                    )

                player_event.total_score_to_par = total_score_to_par
                player_event.todays_score_to_par = todays_score_to_par
                player_event.holes_played_today = holes_played_today

                par = tournament.par
                round_one_to_par = self.get_relative_score(round_one_total_score, par)
                round_two_to_par = self.get_relative_score(round_two_total_score, par)
                round_three_to_par = self.get_relative_score(round_three_total_score, par)
                round_four_to_par = self.get_relative_score(round_four_total_score, par)

                if round_one_to_par is not None:
                    player_event.round_one_to_par=round_one_to_par

                if round_two_to_par is not None:
                    player_event.round_two_to_par=round_two_to_par

                if round_three_to_par is not None:
                    player_event.round_three_to_par=round_three_to_par

                if round_four_to_par is not None:
                    player_event.round_four_to_par=round_four_to_par

                player_event.save()

        self.stdout.write(self.style.SUCCESS("Successfully added player events"))
