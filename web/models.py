import time
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class Wifie(models.Model):
    ssid = models.CharField(max_length=150)
    passworde = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wifis')

    def __str__(self):
        return self.ssid + " " + self.user.username
    class Meta:
        verbose_name = _('Wifi')
        verbose_name_plural = _('Wifies')

class Workshop(models.Model):
    HARDWARE_TYPE = (
        ('1', 'NodeMCU'),
        ('2', 'ESP8266'),
    )
    IDE_TYPE = (
        ('1', 'Arduino IDE'),
        ('2', 'PlatformIO'),
        ('2', _('Other')),
    )
    BUTTON_COLOR_CHOICES=(
        ('btn-outline-success','primary-outline'),
        ('btn-gradient-success','primary-gradient'),
        ('btn-danger','danger'),
        ('btn-outline-danger','danger-outline'),
        ('btn-gradient-danger','danger-gradient'),
        ('btn-dark','dark'),
        ('btn-outline-dark','dark-outline'),
        ('btn-gradient-dark','dark-gradient'),
        ('btn-light','light'),
        ('btn-secondary','secondary'),
        ('btn-outline-secondary','secondary-outline'),
        ('btn-gradient-secondary','secondary-gradient'),
        ('btn-warning','warning'),
        ('btn-outline-warning','warning-outline'),
        ('btn-gradient-warning','warning-gradient'),
        ('btn-info','info'),
        ('btn-outline-info','info-outline'),
        ('btn-gradient-info','info-gradient'),
	)
    hardware = models.CharField(choices=HARDWARE_TYPE, max_length=1,default=HARDWARE_TYPE[0][0], null=True, blank=True)
    ide = models.CharField(choices=IDE_TYPE, max_length=1,default=IDE_TYPE[0][0], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop')
    date_added = models.DateTimeField(auto_now_add=True)
    wifi = models.ForeignKey(Wifie, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=25)
    url = models.CharField(max_length=100)
    detail_url = models.CharField(max_length=100)
    actname = models.CharField(max_length=150)
    def_resp = models.CharField(max_length=150)
    expected_resp = models.CharField(max_length=150)
    current_resp = models.CharField(max_length=150, null=True, blank=True)
    is_fixed = models.BooleanField(default=False)
    duration = models.IntegerField(default=0, help_text=_("turns default in seconds"))
    usage_count = models.IntegerField(default=0)
    button_color = models.CharField(choices=BUTTON_COLOR_CHOICES, max_length=30, default=BUTTON_COLOR_CHOICES[2][0])
    last_used = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _('Workshop')
        verbose_name_plural = _('Workshops')

    def __str__(self):
        return self.user.username + " >---------> " + self.actname

    # list keys of BUTTON_COLOR_CHOICES

    def btns():
        list = []
        for i in Workshop.BUTTON_COLOR_CHOICES:
            list.append(i[0])
        return list
class Workshop_usage(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = _('Workshop usage')
        verbose_name_plural = _('Workshop usages')
    def __str__(self):
        return self.user.username + " >---------> " + self.workshop.actname
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    wifi = models.ForeignKey(Wifie, on_delete=models.CASCADE, related_name="wifi_profile", blank=True, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="workshop_profile", blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

#!NOTE This model is for detecting bad users and analyzing the usage of the website page by page
class UserMovementTrack(models.Model):
    os = models.CharField(max_length=100)
    url =  models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    action =   models.CharField(max_length=150)
    browser =   models.CharField(max_length=100)
    os_name =     models.CharField(max_length=100)
    os_version =   models.CharField(max_length=100)
    is_mobile =   models.CharField(max_length=100)
    is_tablet =   models.CharField(max_length=100)
    is_pc =   models.CharField(max_length=100)
    is_bot =   models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="tracker")
    user_agent = models.CharField(max_length=150, null=True, blank=True)
    language = models.CharField(max_length=100)
    time = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        self.time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username + " >---------> " + self.action

    


