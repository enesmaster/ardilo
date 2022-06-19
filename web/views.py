import re
from turtle import screensize
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, WifiForm,WorkshopCreateForm,CustomLoginForm
from .models import UserMovementTrack, Wifie, Workshop, Workshop_actions
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from api.control_views import *
from django.utils.crypto import get_random_string
chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
import time

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
                'status':_('Incorrect.'),
            }
            return JsonResponse(ctx)

    return render(request, 'web/home.html', {'register_form':register_form, 'workshop_form':workshop_form, 'login_form':login_form})

def configrations(request):
    has_wifi = False
    if request.user.is_authenticated:
        if Wifie.objects.filter(user=request.user).exists():
            has_wifi = True
    if request.method == 'POST' and request.POST.get("operation") == "wifi":
        ssid = request.POST.get("ssid")
        password = request.POST.get("password")
        user = request.POST.get("user")
        # WIFI  
        if Wifie.objects.filter(ssid=ssid,passworde=password, user=User.objects.get(username=user)).exists():
            ctx = {
                'created': False,
                'success': False,
                'status':'duplicate',
                'msg':_('You already have a WiFi with this credentials.<br>If there is a problem delete your exist WiFi on settings and create a new one.<br>Or just update your exist WiFi.'),
            }
            return JsonResponse(ctx)
        Wifie.objects.get_or_create(ssid=ssid,passworde=password, user=User.objects.get(username=user))
        
        this_user_wifies = []
        for i in Wifie.objects.filter(user=request.user).values():
            this_user_wifies.append([(i['id'],i['ssid'])])
        ctx = {
                'user_wifies': this_user_wifies,
                'created': True,
                'success': True,
                'msg': _("You added your WiFi"),
            }
        return JsonResponse(ctx)

    # WORKSHOPS  
    if request.method == 'POST' and request.POST.get("operation") == "workshop":
        actname = request.POST.get("actname")
        def_resp = request.POST.get("def_resp")
        expected_resp = request.POST.get("expected_resp")
        is_fixed = request.POST.get("is_fixed")
        duration = request.POST.get("duration")
        user = User.objects.get(username=request.POST.get("user"))
        if is_fixed == 'true':
            is_fixed = True
        else:
            is_fixed = False
        if Workshop.objects.filter(actname=actname,expected_resp=expected_resp,def_resp=def_resp, user=user).exists():
            ctx = {
                'created': False,
                'success': False,
                'status':'duplicate',
                'msg':_("You already have a Workshop with this credentials.<br>If there is a problem delete your exist Workshop on settings and create a new one <br>Or just update your exist Workshop.")
            }
            return JsonResponse(ctx)
        secret_key = get_random_string(25, chars)
        url = "http://"+request.get_host()+"/workshop/"+secret_key
        detail_url = "http://"+request.get_host()+"/workshop/detail/"+secret_key
        try:
            wifi = Wifie.objects.get(id=request.POST.get("wifi"))
        except:
            return JsonResponse({'created': False,
                'status': False,'msg':_('You need to add a WiFi first before creating a Workshop')})
        Workshop.objects.create(
            actname=actname,
            def_resp=def_resp,
            current_resp=def_resp,
            expected_resp=expected_resp,
            is_fixed=is_fixed,
            duration=duration,
            wifi=wifi,
            user=user,
            secret_key=secret_key,
            url=url,
            detail_url=detail_url
            )
        ctx = {
                'created': True,
                'success': True,
                'secret_key':secret_key,
                'actname':actname,
                'url':url,
                'wifi':Wifie.objects.get(id=request.POST.get("wifi")).ssid,
                'msg':_('You added a Workshop'),
            }
        return JsonResponse(ctx)
    if request.method == 'POST' and request.POST.get("operation") == "get_wifi":
        this_user_wifies = []
        for i in Wifie.objects.filter(user=request.user).values():
            this_user_wifies.append([(i['id'],i['ssid'])])
        ctx = {
                'user_wifies': this_user_wifies,
                'success': True,
            }
        return JsonResponse(ctx)
    if request.method == 'POST' and request.POST.get("operation") == "workshop_json":
        username = request.POST.get("user")
        workshop = Workshop.objects.filter(user=User.objects.get(username=username)).last()
        json = {"username": username ,"action-name":workshop.actname, "wifi": workshop.wifi.ssid, "secret-key": workshop.secret_key, "URL": workshop.url,}
        ctx = {
            'json': json,
            'success': True,
        }
        return JsonResponse(ctx)
    return render(request, 'web/configrations.html' , {'has_wifi':has_wifi})

@login_required
def workshop(request, secret_key):
    workshop = Workshop.objects.get(secret_key=secret_key)
    json = {
        "action-name":workshop.actname,
        "response": workshop.current_resp,
    }
    return JsonResponse(json)

@login_required
def workshop_detail(request, secret_key):
    workshop = Workshop.objects.get(secret_key=secret_key)
    return render(request, "web/detail_workshop.html", {'workshop':workshop})

@login_required
def control_panel(request):
    workshops = Workshop.objects.filter(user=request.user).order_by('-usage_count')
    btns = Workshop.btns
    if request.method == "POST":
        response = "not exist"
        if request.POST.get("operation") == "update-workshop-title":
            response = update_workshop_title(request)
        if request.POST.get("operation") == "delete-workshop":
            response = delete_workshop(request)
        if request.POST.get("operation") == "wake":
            response = wake(request)
        if request.POST.get("operation") == "add-to-home-screen":
            response = add_to_home_screen(request)
        if request.POST.get("operation") == "change-button-color":
            response = change_button_color(request)
        # if request.POST.get("operation") == "update-workshop-duration":
        #   response = update_workshop_duration(request)
        return response
    return render(request, 'web/controls.html', {'workshops':workshops, 'btns':btns})
    
def docs(request):
    return render(request, 'web/docs.html')

def profile(request):
    if request.method == "POST":
        # if request.POST.get("operation") == "update-profile":
        #     return update_profile(request)
        # if request.POST.get("operation") == "update-password":
        #     return update_password(request)
        # if request.POST.get("operation") == "delete-account":
        #     return delete_account(request)
        if request.POST.get("operation") == "dark-mode":
            return dark_mode(request)
    ctx = {
        'last_actions':Workshop_actions.objects.filter(user=request.user).order_by('-date_added')[:5],
        'most_used_workshops':Workshop.objects.filter(user=request.user).order_by('usage_count')[:5],
    }
    return render(request, 'user/profile.html', ctx)

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

def not_found404(request, exception):
        data = {}
        return render(request,'web/404.html', data)
 