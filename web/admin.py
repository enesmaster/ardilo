from django.contrib import admin
from .models import Profile, Wifi, Workshop

admin.site.register(Workshop)
admin.site.register(Wifi)
admin.site.register(Profile)