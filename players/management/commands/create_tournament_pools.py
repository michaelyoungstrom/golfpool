import csv

from django.core.management.base import BaseCommand
from players.models import Player, Pool
from tournaments.models import Tournament

"""
Parses a csv file to add pools for a tournament.

Assumes a csv file with the following format (one line):
    tournament_id, pool_id, player_first_name, player_last_name

Additionally, this file will update additional values in the csv row if you choose to add score for each round
"""
class Command(BaseCommand):
    help = 'Adds pools to a tournament'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help="Relative path to csv file containing pools for a tournament")

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file) as csv_file_object:
            csv_reader = csv.reader(csv_file_object, delimiter=',')
            for row in csv_reader:
                tournament_id = row[0]
                pool_id = row[1]
                player_first_name = row[2]
                player_last_name = row[3]

                try:
                    tournament = Tournament.objects.get(tournament_id=tournament_id)
                except Tournament.DoesNotExist:
                    raise ValueError(
                        "Tournament with id: {} not found.".format(tournament_id)
                    )

                try:
                    player = Player.objects.get(first_name=player_first_name, last_name=player_last_name)
                except Player.DoesNotExist:
                    raise ValueError(
                        "Player: {} {} not found.".format(player_first_name, player_last_name)
                    )

                try:
                    pool = Pool.objects.get(
                        pool_id=pool_id,
                        tournament=tournament
                    )
                except Pool.DoesNotExist:
                    pool = Pool(
                        pool_id=pool_id,
                        tournament=tournament
                    )
                    pool.save()

                pool.players.add(player)
                pool.save()

        self.stdout.write(self.style.SUCCESS("Successfully added player events"))
