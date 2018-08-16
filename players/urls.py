from django.conf.urls import url
from . import views

app_name = 'players'

urlpatterns = [
    url(r'^(?P<tournament_key>[0-9]+)/selection/', views.player_selection, name='selection'),
    url(r'^(?P<tournament_key>[0-9]+)/submit/', views.create_or_update_user_event, name='submit'),
]
