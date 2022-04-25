from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,WorkshopCreateForm,CustomLoginForm
from .models import Wifi, Workshop
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

#! TODO add api views to api
def home(request):
    register_form = RegisterForm()
    login_form = CustomLoginForm()
    workshop_form = WorkshopCreateForm
    if request.method == 'POST' and request.POST.get("operation") == "register":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
 
            ctx = {
                'username': register_form.cleaned_data['username'],
                'password': register_form.cleaned_data['password1'],
                'created': True,
                'success': True,
                'msg':'You created your account',
            }
            return JsonResponse(ctx)
        else:
            ctx = {
                'username': '',
                'password': '',
                'created': False,
                'success': False,
                'status':'error',
                'msg': _('Passwords do not match')
            }
            return JsonResponse(ctx)
            
    elif request.method == 'POST' and request.POST.get("operation") == "login":
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            message = _('Hello %(username)s ! You have been logged in') % {'username': user.username}
            ctx = {
                'created': True,
                'success': True,
                'status':message,
                'username': user.username,
                
            }
            return JsonResponse(ctx)
        else:
            ctx = {
                'created': False,
                'success': False,
                'status':'Incorrect.',
            }
            return JsonResponse(ctx)

    return render(request, 'web/home.html', {'register_form':register_form, 'workshop_form':workshop_form, 'login_form':login_form})

def configrations(request):
    if request.method == 'POST' and request.POST.get("operation") == "wifi":
        ssid = request.POST.get("ssid")
        password = request.POST.get("password")
        Wifi.objects.create(ssid=ssid, password=password, user=request.user)
        return JsonResponse({'success':True, 'msg':'Wifi configuration created'})
    return render(request, 'web/configrations.html')
    
def docs(request):
    return render(request, 'web/docs.html')

def profile(request):
    return render(request, 'web/docs.html')

@login_required
def open_the_door(request):
    if request.method == 'POST' and request.POST.get("operation") == "open_the_door":
        a = Workshop.objects.create(user=request.user,is_open = True)
        a.is_open = True
        a.save()
        return JsonResponse({"is_open":a.is_open})
    if request.method == 'POST' and request.POST.get("operation") == "close_the_door":
        a = Workshop.objects.filter(user=request.user).last()
        a.is_open = False
        a.save()
        return JsonResponse({"is_open":a.is_open})
    return render(request, 'otd.html')


class LoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

