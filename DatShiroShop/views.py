from django.conf.urls import url
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from DatShiroShop.models import Song
from api.drive_api import list_files, get_file, load_files_to_sqlite, downloadFile


def home(request):
    songs = Song.objects.all()
    # load_files_to_sqlite()
    # list_files()
    return render(request, 'index.html', {'songs': songs})


def download(request, song_id):
    song = Song.objects.get(pk=song_id)
    print("Start download file name: " + song.name)
    downloadFile(song_id, song.name + " - " + song.author)
    print("Downloaded")
    return HttpResponseRedirect(request.GET.get('return_url'))

