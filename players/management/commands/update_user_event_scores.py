import click

from django.core.management.base import BaseCommand
from players.models import Player, PlayerEvent, UserEvent
from tournaments.models import Tournament
from django.db.models import F
"""
Update UserEvent scores, which will update the current leaderboard standings
"""
class Command(BaseCommand):
    help = 'Adds player events to database'

    def add_arguments(self, parser):
        parser.add_argument('tournament_name', help="Name of the tournament to update")
        parser.add_argument('tournament_year', help="Year of the tournament to update")

    def handle(self, *args, **options):
        tournament_name = options['tournament_name']
        tournament_year = options['tournament_year']

        try:
            tournament = Tournament.objects.get(name=tournament_name, start_date__year=tournament_year)
        except Tournament.DoesNotExist:
            raise ValueError(
                "Tournament not found. Please make sure there exists an entry in Tournaments with the desired name and year"
            )

        user_events = UserEvent.objects.filter(tournament=tournament)
        for event in user_events:
            round_one_score = 0
            for player_event in event.player_events.all().order_by(F('round_one_to_par').asc(nulls_last=True))[:tournament.day_one_score_count]:
                player_round_one_score = player_event.round_one_to_par
                if player_round_one_score:
                    round_one_score = round_one_score + player_event.round_one_to_par

            round_two_score = 0
            for player_event in event.player_events.all().order_by(F('round_two_to_par').asc(nulls_last=True))[:tournament.day_two_score_count]:
                player_round_two_score = player_event.round_two_to_par
                if player_round_two_score:
                    round_two_score = round_two_score + player_event.round_two_to_par

            round_three_score = 0
            for player_event in event.player_events.all().order_by(F('round_three_to_par').asc(nulls_last=True))[:tournament.day_three_score_count]:
                player_round_three_score = player_event.round_three_to_par
                if player_round_three_score:
                    round_three_score = round_three_score + player_event.round_three_to_par

            round_four_score = 0
            for player_event in event.player_events.all().order_by(F('round_four_to_par').asc(nulls_last=True))[:tournament.day_four_score_count]:
                player_round_four_score = player_event.round_four_to_par
                if player_round_four_score:
                    round_four_score = round_four_score + player_event.round_four_to_par

            event.round_one_to_par = round_one_score
            event.round_two_to_par = round_two_score
            event.round_three_to_par = round_three_score
            event.round_four_to_par = round_four_score
            event.total_score_to_par = round_one_score + round_two_score + round_three_score + round_four_score
            event.save()

        last_score = None
        for position_counter, event in enumerate(user_events.order_by('total_score_to_par'), 1):
            current_score = event.total_score_to_par
            if current_score == last_score:
                event.position = last_position
            else:
                event.position = position_counter
                last_position = position_counter
                last_score = current_score
            event.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated UserEvent scores"))
