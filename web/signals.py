from django.db.models.signals import post_save, pre_save,post_delete
from django.conf import settings 
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from . models import Profile, UserMovementTrack, Workshop, Workshop_actions
import datetime
import time
User = settings.AUTH_USER_MODEL


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(user_logged_in)
def user_logged(sender,request,user,**kwargs):
    
    #||==> Profile
    user.profile.is_online = True
    user.profile.last_login = datetime.datetime.now()
    user.profile.save()

    #||==> Tracker
    UserMovementTrack.objects.create(
        user = user,
        os = request.user_agent.os,
        os_name = request.user_agent.os.family,
        os_version = request.user_agent.os.version,
        device = request.user_agent.device.family,
        action = "log_in",
        browser = request.user_agent.browser.family,
        is_mobile = request.user_agent.is_mobile ,
        is_tablet = request.user_agent.is_tablet,
        is_pc = request.user_agent.is_pc,
        is_bot = request.user_agent.is_bot,
        language=request.LANGUAGE_CODE,
        ip = get_client_ip(request),
        url= "login/"
    )


@receiver(user_logged_out)
def user_logged_out(sender,request,user,**kwargs):
    user.profile.is_online = False
    user.profile.save()
        #||==> Tracker
    UserMovementTrack.objects.create(
        user = user,
        os = request.user_agent.os,
        os_name = request.user_agent.os.family,
        os_version = request.user_agent.os.version,
        device = request.user_agent.device.family,
        action = "log_out",
        browser = request.user_agent.browser.family,
        is_mobile = request.user_agent.is_mobile ,
        is_tablet = request.user_agent.is_tablet,
        is_pc = request.user_agent.is_pc,
        is_bot = request.user_agent.is_bot,
        language=request.LANGUAGE_CODE,
        ip = get_client_ip(request),
        url= "logout/"
    )

@receiver(post_save, sender=Workshop)
def action_post(sender, instance, created, **kwargs):
    if created:
        Workshop_actions.objects.create(
            workshop=instance.actname,
            user=instance.user,
            action=Workshop_actions.WORKSHOP_ACTIONS[0][0]
            )
    else:
        Workshop_actions.objects.create(
            workshop=instance.actname,
            user=instance.user,
            action=Workshop_actions.WORKSHOP_ACTIONS[1][0]
            )

@receiver(post_delete, sender=Workshop)
def action_delete(sender, instance, **kwargs):
    Workshop_actions.objects.create(
        workshop=instance.actname,
        user=instance.user,
        action=Workshop_actions.WORKSHOP_ACTIONS[2][0]
        )

@receiver(post_save, sender=Workshop)
def last_used_act(sender, instance, **kwargs):
    instance.last_used = timezone.now()

# @receiver(post_save, sender=Workshop)
# def update_response(sender, instance, **kwargs):
#     if instance.is_fixed == True:
#         time.sleep(instance.duration)
#         instance.current_resp = instance.def_resp
#         instance.save()