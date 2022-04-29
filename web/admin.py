from django.contrib import admin
from .models import Profile, Wifie, Workshop

admin.site.register(Workshop)
admin.site.register(Wifie)
admin.site.register(Profile)