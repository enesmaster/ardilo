from django.db.models.signals import post_save, pre_save
from django.conf import settings 
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from . models import Profile, Workshop
import datetime

User = settings.AUTH_USER_MODEL


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
    user.profile.is_online = True
    user.profile.last_login = datetime.datetime.now()
    user.profile.save()

@receiver(user_logged_out)
def user_logged_out(sender,request,user,**kwargs):
    user.profile.is_online = False
    user.profile.save()

@receiver(post_save, sender=Workshop)
def update_response(sender, instance, **kwargs):
    if instance.is_fixed == True:
        instance.current_resp = instance.def_resp
        instance.save()