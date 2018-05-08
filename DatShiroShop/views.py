from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from DatShiroShop.models import Song
from api.drive_api import list_files, get_file, load_files_to_sqlite


def home(request):
    songs = Song.objects.all()
    # load_files_to_sqlite()
    return render(request, 'index.html', {'songs':songs} )
