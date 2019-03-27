from django import forms
from .models import ContactMe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User



class ContactMeForm(forms.ModelForm):

    class Meta:
        model = ContactMe
        fields = ('senderEmail', 'message',)