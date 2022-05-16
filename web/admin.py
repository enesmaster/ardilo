from django.contrib import admin
from .models import Profile, Wifie, Workshop, Workshop_usage

admin.site.register(Workshop)
admin.site.register(Workshop_usage)
admin.site.register(Wifie)
admin.site.register(Profile)