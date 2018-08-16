from django.contrib import admin
from . import models

admin.site.register(models.Player)
admin.site.register(models.PlayerEvent)
admin.site.register(models.UserEvent)
