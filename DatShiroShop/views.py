import os

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from DatShiroShop.forms import UploadFileForm, SignUpForm
from DatShiroShop.models import Song, Profile
from api.drive_api import list_files, get_file, load_files_to_sqlite, downloadFile, uploadFile


def home(request):
    songs = Song.objects.all()
    user_id = request.session.get('user_id', None)
    user = None
    if user_id:
        user = Profile.objects.get(user=user_id)
    return render(request, 'index.html', {'songs': songs, 'user': user})


def download(request, song_id):
    song = Song.objects.get(pk=song_id)
    print("Start download file name: " + song.name)
    downloadFile(song_id, song.name + " - " + song.author)
    print("Downloaded")
    return HttpResponseRedirect(request.GET.get('return_url'))


def upload(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            price = form.cleaned_data['price']
            my_file = request.FILES['myFile']
            extension = my_file.name.rsplit('.', 1)[1]
            file_id = uploadFile(name + " - " + author + "." + extension, my_file.temporary_file_path(), my_file.content_type)
            new_song = Song(id=file_id, name=name, author=author, extension=extension, price=price)
            new_song.save()
            return redirect('homepage')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'sites/signup.html', {'form':form})


@login_required
def buy_song(request, song_id):
    #Get Song From Drive
    print("Start buy music")
    file_path = os.path.expanduser(os.sep.join(["~", "Downloads"]))
    downloaded_file_path = downloadFile(song_id, file_name=song_id + str(request.session.get('user_id', None)), file_path=file_path)
    song_file = open(downloaded_file_path, 'rb')
    read_file = (song_file.read())
    #Sign Signature To Song
    #Upload Song to User Folder
    #Update Archived Song to Profile
    #Delete signed song on local
    # return signed_song
    return HttpResponse(read_file)
    pass