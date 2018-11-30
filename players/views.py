from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tournaments.models import Tournament
from players.models import PlayerEvent, UserEvent

@login_required
def player_selection(request, tournament_key, player_selection_error=None):
    """
    Shows current selections (if there are any) for a tournament and allows
    users to submit changes.
    """
    tournament = Tournament.objects.get(pk=tournament_key)
    user_player_events = []
    try:
        user_event = UserEvent.objects.get(user=request.user, tournament=tournament)
        user_player_events = user_event.player_events.all()
    except:
        pass
    player_events_group_list = []
    for pool in range(1, tournament.number_of_pools + 1):
        player_events_group_list.append(PlayerEvent.objects.filter(tournament=tournament, pool=pool))
    return render(
        request,
        'players/players_selection.html',
        {
            'tournament': tournament,
            'player_events_group_list': player_events_group_list,
            'user_player_events': user_player_events,
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
            user_event.player_events.clear()
        except:
            user_event = UserEvent(user=request.user, tournament=tournament, total_score_to_par=0)
            user_event.save()
        for pool in range(1, tournament.number_of_pools + 1):
            try:
                player_event_id = int(request.POST['pool_' + str(pool)])
            except:
                msg = """Error: Missing at least one pool selection. Please make sure you make a
                selection for each pool and resubmit."""
                return player_selection(request, tournament_key, msg)
            user_event.player_events.add(PlayerEvent.objects.get(pk=player_event_id))
    return redirect('tournaments:overview', pk=tournament.id)
