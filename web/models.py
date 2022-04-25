from django.db import models
from django.contrib.auth.models import User

class Wifi(models.Model):
    ssid = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ssid + " " + self.user.username

class Workshop(models.Model):
    HARDWARE_TYPE = (
        ('1', 'NodeMCU'),
        ('2', 'ESP8266'),
    )
    IDE_TYPE = (
        ('1', 'Arduino IDE'),
        ('2', 'PlatformIO'),
        ('2', 'Other'),
    )
    hardware = models.CharField(choices=HARDWARE_TYPE, max_length=1,default=HARDWARE_TYPE[0][0])
    ide = models.CharField(choices=IDE_TYPE, max_length=1,default=IDE_TYPE[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    ssid = models.ForeignKey(Wifi, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=12)
    signal = models.BooleanField(default=False)
    def __str__(self):
        return self.hardware

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    wifi = models.ForeignKey(Wifi, on_delete=models.CASCADE, related_name="wifi_profile", blank=True, null=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="workshop_profile", blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    