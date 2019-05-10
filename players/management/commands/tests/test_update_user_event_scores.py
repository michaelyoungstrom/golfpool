"""
Tests for management command that updates user event scores
"""
from django.test import TestCase
from django.core.management import call_command

from mock import Mock, patch, MagicMock

class TestUpdateUserEventScores(TestCase):

    @patch('players.management.commands.update_user_event_scores.Command.calculate_round_score', side_effect=[0, -2, 3, -3])
    @patch('players.management.commands.update_user_event_scores.Command.get_max_score_in_round', return_value=10)
    @patch('tournaments.models.Tournament', return_value=Mock())
    def test_happy_path(self, tournament_mock, max_score_mock, calculate_round_mock):
        user_events = MagicMock()
        user_events.__iter__.return_value = [Mock()]
        user_events.order_by.__iter__.return_value = [Mock()]
        with patch('players.models.UserEvent.objects.filter', return_value=user_events):
            call_command('update_user_event_scores', '1')
            assert user_events.__iter__.return_value[0].total_score_to_par == -2
