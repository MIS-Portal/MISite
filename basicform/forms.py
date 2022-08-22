from django.forms import ModelForm
from .models import Student
from django import forms
class AdminForm(forms.Form):
    uid=forms.CharField()
   