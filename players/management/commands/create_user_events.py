import csv

from django.core.management.base import BaseCommand
from players.models import Player, PlayerEvent, UserEvent
from tournaments.models import Tournament
from django.contrib.auth.models import User

"""
Parses a csv file to user events to a tournament.

Assumes a csv file with the following format (one line):
    user_last_name, user_first_name, tournament_id, player_first_name, player_last_name

Chacnes are, this management command won't be useful in the long run. This is more to help
in the short term, as I mirror golfpools for testing.
"""
class Command(BaseCommand):
    help = 'Adds user events to database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help="Relative path to csv file containing user event data")
        parser.add_argument('num_players', type=int, help="Number of players to select for this tournament")

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        num_players = options['num_players']
        with open(csv_file) as csv_file_object:
            csv_reader = csv.reader(csv_file_object, delimiter=',')
            for row in csv_reader:
                user_first_name = row[0]
                user_last_name = row[1]
                tournament_id = row[2]
                players_dict = {}
                for num in range(1, num_players+1):
                    players_dict["player_{}".format(num)] = row[2+num]

                # Just going to create dummy users for now, this won't make sense in reality
                username = "{}_{}".format(user_first_name, user_last_name)
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        email="{}_{}@gmail.com".format(user_first_name, user_last_name),
                        username=username,
                        first_name=user_first_name,
                        last_name=user_last_name,
                        password="dummy_password",
                    )
                user.save()

                try:
                    tournament = Tournament.objects.get(tournament_id=tournament_id)
                except Tournament.DoesNotExist:
                    raise ValueError(
                        "Tournament with id: {} not found.".format(tournament_id)
                    )

                try:
                    user_event = UserEvent.objects.get(
                        user=user,
                        tournament=tournament
                    )
                except UserEvent.DoesNotExist:
                    user_event = UserEvent(
                        user=user,
                        tournament=tournament
                    )
                user_event.save()

                players = []
                for number in range(1, num_players+1):
                    player_full_name_list = players_dict["player_{}".format(number)].split(" ")
                    player_first = player_full_name_list[0]
                    player_last = " ".join(player_full_name_list[1:])
                    try:
                        player = Player.objects.get(
                            first_name=player_first,
                            last_name=player_last
                        )
                        players.append(player)
                    except Player.DoesNotExist:
                        raise ValueError(
                            "Player {} {} not found.".format(player_first, player_last)
                        )

                user_event.players=players
                user_event.save()

        self.stdout.write(self.style.SUCCESS("Successfully added user events"))
