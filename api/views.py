from django.shortcuts import render
from django.http import JsonResponse
from web.models import Workshop, Wifie, Profile
from django.contrib.auth.decorators import login_required

@login_required
def api_door_view(request):
    a = Workshop.objects.last()
    return JsonResponse({'signal':a.signal})