from django.core.management.base import BaseCommand
from players.models import Player, PlayerEvent, UserEvent
from tournaments.models import Tournament
from django.db.models import F
"""
Update UserEvent scores, which will update the current leaderboard standings
"""
class Command(BaseCommand):
    help = 'Adds player events to database'
    round_dict = {
        1: 'round_one_to_par',
        2: 'round_two_to_par',
        3: 'round_three_to_par',
        4: 'round_four_to_par'
    }

    def add_arguments(self, parser):
        parser.add_argument('tournament_id', help="Id of the tournament to update")

    def calculate_round_score(self, players, round, tournament, num_scores_count):
        if round not in self.round_dict:
            raise ValueError(
                "Not a valid round number"
            )

        round_attribute = self.round_dict[round]
        total_round_score = 0
        for player_event in PlayerEvent.objects.filter(tournament=tournament, player__in=players).order_by(F(round_attribute).asc(nulls_last=True))[:num_scores_count]:
            round_score = getattr(player_event, round_attribute)
            if round_score is not None:
                total_round_score += round_score
        return total_round_score

    def handle(self, *args, **options):
        tournament_id = options['tournament_id']

        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
        except Tournament.DoesNotExist:
            raise ValueError(
                "Tournament not found."
            )

        user_events = UserEvent.objects.filter(tournament=tournament)
        for event in user_events:

            players = event.players.all()

            event.round_one_to_par = self.calculate_round_score(players, 1, tournament, tournament.day_one_score_count)
            event.round_two_to_par = self.calculate_round_score(players, 2, tournament, tournament.day_two_score_count)
            event.round_three_to_par = self.calculate_round_score(players, 3, tournament, tournament.day_three_score_count)
            event.round_four_to_par = self.calculate_round_score(players, 4, tournament, tournament.day_four_score_count)

            event.total_score_to_par = event.round_one_to_par + event.round_two_to_par + event.round_three_to_par + event.round_four_to_par
            event.save()

        last_score = None
        for position_counter, event in enumerate(user_events.order_by('total_score_to_par'), 1):
            current_score = event.total_score_to_par
            if last_score and current_score == last_score:
                event.position = last_position
            else:
                event.position = position_counter
                last_position = position_counter
                last_score = current_score
            event.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated UserEvent scores"))
