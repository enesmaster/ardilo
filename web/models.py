from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
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
    hardware = models.CharField(choices=HARDWARE_TYPE, max_length=1,default=HARDWARE_TYPE[0][0], null=True, blank=True)
    ide = models.CharField(choices=IDE_TYPE, max_length=1,default=IDE_TYPE[0][0], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop')
    date_added = models.DateTimeField(auto_now_add=True)
    wifi = models.ForeignKey(Wifie, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=25)
    url = models.CharField(max_length=100)
    actname = models.CharField(max_length=150)
    def_resp = models.CharField(max_length=150)
    expected_resp = models.CharField(max_length=150)
    current_resp = models.CharField(max_length=150, null=True, blank=True)
    is_fixed = models.BooleanField(default=False)
    duration = models.IntegerField(default=0, help_text=_("turns default in seconds"))
    usage_count = models.IntegerField(default=0)
    class Meta:
        verbose_name = _('Workshop')
        verbose_name_plural = _('Workshops')

    def __str__(self):
        return self.user.username + " >---------> " + self.actname

    def save(self, *args, **kwargs):
        self.current_resp = self.def_resp
        super(Workshop, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    wifi = models.ForeignKey(Wifie, on_delete=models.CASCADE, related_name="wifi_profile", blank=True, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="workshop_profile", blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')