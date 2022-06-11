from django.contrib import admin
from .models import Profile, Wifie, Workshop, Workshop_actions,UserMovementTrack

admin.site.register(Workshop)
admin.site.register(Workshop_actions)
admin.site.register(Wifie)
admin.site.register(Profile)
admin.site.register(UserMovementTrack)