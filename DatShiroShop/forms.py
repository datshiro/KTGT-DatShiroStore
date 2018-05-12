from django import forms
from django.forms import CharField, Textarea, TextInput, FileField, FileInput

from DatShiroShop.models import Song


class UploadFileForm(forms.ModelForm):
    myFile = FileField(label='Song File', widget=FileInput(attrs={'onChange': 'getFileInfo()'}))

    class Meta:
        model = Song
        fields = ['myFile', 'name', 'author', 'price']
