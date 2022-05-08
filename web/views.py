from random import random
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, WifiForm,WorkshopCreateForm,CustomLoginForm
from .models import Wifie, Workshop
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
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
        Workshop.objects.create(
            actname=actname,
            def_resp=def_resp,
            current_resp=def_resp,
            expected_resp=expected_resp,
            is_fixed=is_fixed,
            duration=duration,
            wifi=Wifie.objects.get(id=request.POST.get("wifi")),
            user=user,
            secret_key=secret_key,
            url=url
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
    return render(request, 'web/configrations.html')

@login_required
def workshop(request, secret_key):
    workshop = Workshop.objects.get(secret_key=secret_key)
    json = {
        "action-name":workshop.actname,
        "response": workshop.current_resp,
    }
    return JsonResponse(json)

@login_required
def control_panel(request):
    workshops = Workshop.objects.filter(user=request.user).order_by('-usage_count')
    if request.method == 'POST' and request.POST.get("operation") == "wake":
        a = Workshop.objects.get(id=request.POST.get("workshop_id"))
        is_duration = False
        if a.current_resp == a.def_resp:
            a.current_resp=request.POST.get("workshop_exp")
            resp_btn = a.def_resp
            if a.is_fixed == False:
                is_duration = True
                time.sleep(a.duration)
                a.current_resp='ff'

        else:
            a.current_resp=request.POST.get("workshop_def")
            resp_btn = a.expected_resp

        a.usage_count += 1
        a.save()
        print(a.current_resp)
        ctx={
            'success': True,
            'duration': a.duration,
            'is_duration': is_duration,
            'response': a.current_resp,
            'resp_btn': resp_btn,
        }
        return JsonResponse(ctx)
    if request.method == 'POST' and request.POST.get("operation") == "delete-workshop":
        a = Workshop.objects.get(id=request.POST.get("workshop_id"))
        a.delete()
        ctx={
            'success': True,
            'msg': _('Deleting...'),
            'workshop_id': request.POST.get("workshop_id"),
        }
        return JsonResponse(ctx)
    return render(request, 'web/controls.html', {'workshops':workshops})
 
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

