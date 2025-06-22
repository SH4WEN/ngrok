from django import forms
from .models import SharedFile, EmailMessage
from django.contrib.auth.models import User

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['file', 'description']

class EmailForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = EmailMessage
        fields = ['recipient', 'subject', 'body']