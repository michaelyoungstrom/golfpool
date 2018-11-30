from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tournament
from players.models import PlayerEvent, UserEvent

def home(request):
    tournaments = Tournament.objects.order_by('-start_date')
    return render(request, 'tournaments/home.html', {'tournaments': tournaments})

def overview(request, pk):
    tournament = Tournament.objects.get(pk=pk)
    user_events = UserEvent.objects.filter(tournament=tournament).order_by('total_score_to_par')
    user_has_entry = False
    try:
        request_user_event = UserEvent.objects.get(user=request.user, tournament=tournament)
        user_has_entry = True
    except:
        pass
    return render(
        request,
        'tournaments/overview.html',
        {
            'request_user': request.user,
            'tournament': tournament,
            'user_events': user_events,
            'user_has_entry': user_has_entry
        }
    )
