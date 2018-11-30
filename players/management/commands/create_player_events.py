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

    def get_round_score(self, csv_row, num):
        """
        Get value of csv_row at num, or None if it doesn't exist
        """
        try:
            score = csv_row[num]
        except:
            score = None

        return score

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file) as csv_file_object:
            csv_reader = csv.reader(csv_file_object, delimiter=',')
            for row in csv_reader:
                tournament_name = row[0]
                tournament_year = row[1]
                first_name = row[2]
                last_name = row[3]
                pool = row[4]
                round_one_to_par = self.get_round_score(row, 5)
                round_two_to_par = self.get_round_score(row, 6)
                round_three_to_par = self.get_round_score(row, 7)
                round_four_to_par = self.get_round_score(row, 8)

                try:
                    player = Player.objects.get(first_name=first_name, last_name=last_name)
                except Player.DoesNotExist:
                    raise ValueError(
                        "Player {} {} not found. Please make sure the first and last name match an entry in the Players database.".format(first_name, last_name)
                    )

                try:
                    tournament = Tournament.objects.get(name=tournament_name, start_date__year=tournament_year)
                except Tournament.DoesNotExist:
                    raise ValueError(
                        "Tournament {} {} not found. Please make sure there exists an entry in Tournaments with the desired name and year".format(tournament_name, tournament_year)
                    )

                if int(pool) > tournament.number_of_pools:
                    raise ValueError(
                        "Invalid pool number {}. Make sure the tournament has a valid number of pools, and that this "
                        "pool number is within that range.".format(int(pool))
                    )

                try:
                    player_event = PlayerEvent.objects.get(
                        tournament=tournament,
                        player=player,
                        pool=pool
                    )
                except PlayerEvent.DoesNotExist:
                    player_event = PlayerEvent(
                        tournament=tournament,
                        player=player,
                        pool=pool
                    )

                if round_one_to_par:
                    player_event.round_one_to_par=round_one_to_par

                if round_two_to_par:
                    player_event.round_two_to_par=round_two_to_par

                if round_three_to_par:
                    player_event.round_three_to_par=round_three_to_par

                if round_four_to_par:
                    player_event.round_four_to_par=round_four_to_par

                player_event.save()

        self.stdout.write(self.style.SUCCESS("Successfully added player events"))
