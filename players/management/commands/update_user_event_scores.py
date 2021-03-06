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

    def get_max_score_in_round(self, tournament, round):
        round_attribute = self.round_dict[round]
        max_player = PlayerEvent.objects.filter(tournament=tournament).order_by("-{}".format(round_attribute))[0]
        max_player_score = getattr(max_player, round_attribute)

        return max_player_score if max_player_score is not None else 0

    def calculate_round_score(self, players, round, tournament, num_scores_count, max_player_score):
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
            else:
                player_total_score_to_par = player_event.total_score_to_par
                try:
                    # If we can get a total score thats an int, the player is still active
                    if player_total_score_to_par != "E":
                        int(player_total_score_to_par)
                except:
                    # we're hitting players that are no longer playing, add max player score
                    total_round_score += max_player_score
        return total_round_score

    def handle(self, *args, **options):
        tournament_id = options['tournament_id']
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
        except Tournament.DoesNotExist:
            raise ValueError(
                "Tournament not found."
            )

        first_round_max = self.get_max_score_in_round(tournament, 1)
        second_round_max = self.get_max_score_in_round(tournament, 2)
        third_round_max = self.get_max_score_in_round(tournament, 3)
        fourth_round_max = self.get_max_score_in_round(tournament, 4)

        user_events = UserEvent.objects.filter(tournament=tournament)
        for event in user_events:
            players = event.players.all()

            event.round_one_to_par = self.calculate_round_score(players, 1, tournament, tournament.day_one_score_count, first_round_max)
            event.round_two_to_par = self.calculate_round_score(players, 2, tournament, tournament.day_two_score_count, second_round_max)
            event.round_three_to_par = self.calculate_round_score(players, 3, tournament, tournament.day_three_score_count, third_round_max)
            event.round_four_to_par = self.calculate_round_score(players, 4, tournament, tournament.day_four_score_count, fourth_round_max)

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
