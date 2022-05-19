import time
from django.http import JsonResponse
from django.contrib.auth.models import User
from web.models import Wifie, Workshop
from django.utils.translation import gettext_lazy as _

def update_workshop_title(request):
    a = Workshop.objects.get(id=request.POST.get("workshop_id"))
    #a.duration = request.POST.get("duration")
    a.actname = request.POST.get("new_name")
    a.save()
    ctx={
        'success': True,
        'msg': _('Updating...'),
        'new_name': request.POST.get("new_name"),
    }
    return JsonResponse(ctx)

def delete_workshop(request):
    try:
        a = Workshop.objects.get(id=request.POST.get("workshop_id"))
        a.delete()
    except Workshop.DoesNotExist:
        pass
    ctx={
        'success': True,
        'status':'deleted',
        'msg': _('Deleting...'),
        'workshop_id': request.POST.get("workshop_id"),
    }
    return JsonResponse(ctx)
    
def change_button_color(request):
    a = Workshop.objects.get(id=request.POST.get("workshop_id"))
    buton_color = int(request.POST.get("button_color"))
    a.button_color = Workshop.BUTTON_COLOR_CHOICES[buton_color-1][0]
    a.save()
    ctx={
        'success': True,
        'status':'ok',
        'color_id': a.button_color,
        'msg': _('Deleting...'),
        'workshop_id': request.POST.get("workshop_id"),
    }
    return JsonResponse(ctx)

def wake(request):
    a = Workshop.objects.get(id=request.POST.get("workshop_id"))
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
    ctx={
        'success': True,
        'duration': a.duration,
        #'is_duration': is_duration,
        'response': a.current_resp,
        'resp_btn': resp_btn,
    }
    return JsonResponse(ctx)