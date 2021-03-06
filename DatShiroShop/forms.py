from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, Textarea, TextInput, FileField, FileInput

from DatShiroShop.models import Song


class UploadFileForm(forms.ModelForm):
    myFile = FileField(label='Song File', widget=FileInput(attrs={'onChange': 'getFileInfo()'}))

    class Meta:
        model = Song
        fields = ['myFile', 'name', 'author', 'price']


class GetSignatureForm(forms.Form):
    myFile = FileField(label='Song File')


class LoginForm(forms.Form):
    email = CharField(min_length=1, max_length=100)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
