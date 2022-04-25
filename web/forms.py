from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Workshop


class WorkshopCreateForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['hardware','ide']

        def __init__(self, *args, **kwargs):
            super(WorkshopCreateForm, self).__init__(*args, **kwargs)

        
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput())
        
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control"}))
    
    email.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control"}))

class UserChangeForm(UserChangeForm):
    username = forms.CharField(label='subject', max_length=100 , widget=forms.TextInput(
        attrs={'class': "form-control"}))


    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name']
        
        def __init__(self, *args, **kwargs):
            super(UserChangeForm, self).__init__(*args, **kwargs)
            for fieldname in ['username', 'email', 'first_name', 'last_name']:
                self.fields[fieldname].attrs['class'] = 'form-control'