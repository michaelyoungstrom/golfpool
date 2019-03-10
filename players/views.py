from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tournaments.models import Tournament
from players.models import Player, UserEvent, Pool

@login_required
def player_selection(request, tournament_key, player_selection_error=None):
    """
    Shows current selections (if there are any) for a tournament and allows
    users to submit changes.
    """
    tournament = Tournament.objects.get(pk=tournament_key)
    user_players = []
    try:
        user_event = UserEvent.objects.get(user=request.user, tournament=tournament)
        user_players = user_event.players.all()
    except:
        pass
    pools = Pool.objects.filter(tournament=tournament_key)
    return render(
        request,
        'players/players_selection.html',
        {
            'tournament': tournament,
            'pools': pools,
            'user_players': user_players,
            'player_selection_error': player_selection_error
        }
    )

def create_or_update_user_event(request, tournament_key, error=None):
    """
    Creates or modifies a User's UserEvent for a tournament. This is only
    allowed before a tournament has actually begun, and required a selection of one player
    per pool.
    """
    tournament = Tournament.objects.get(pk=tournament_key)
    if request.method == 'POST':
        try:
            user_event = UserEvent.objects.get(user=request.user, tournament=tournament)
            user_event.players.clear()
        except:
            user_event = UserEvent(user=request.user, tournament=tournament, total_score_to_par=0)
            user_event.save()
        pools = Pool.objects.filter(tournament=tournament)
        for pool in pools:
            try:
                player_id = int(request.POST['pool_' + pool.pool_id])
                player = Player.objects.get(player_id=player_id)
            except:
                msg = """Error: Missing at least one pool selection. Please make sure you make a
                selection for each pool and resubmit."""
                return player_selection(request, tournament_key, msg)
            user_event.players.add(player)
    return redirect('tournaments:overview', pk=tournament.tournament_id)
