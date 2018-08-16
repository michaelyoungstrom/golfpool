from django.conf.urls import url
from . import views

app_name = 'tournaments'

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)', views.overview, name='overview'),
]
