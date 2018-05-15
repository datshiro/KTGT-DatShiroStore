import operator
import os
from functools import reduce

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from DatShiroShop.forms import UploadFileForm, SignUpForm
from DatShiroShop.models import Song, Profile
from api import drive_api
from api.drive_api import list_files, get_file, load_files_to_sqlite, downloadFile, uploadFile, createFolder, deleteFile


def home(request):
    list_songs = list_files()
    songs = []
    for song in list_songs:
        s = Song.objects.get(pk=song['id'])
        songs.append(s)
    user_id = request.session.get('user_id', None)
    user = User.objects.get(pk=user_id) if user_id else None
    user_name_songs = [song['name'] for song in user.profile.songs.values()] if user else []
    return render(request, 'index.html', {'songs': songs, 'user': user, 'user_name_songs': user_name_songs})


def download(request, song_id):
    song = Song.objects.get(pk=song_id)
    print("Start download file name: " + song.name)
    downloadFile(song_id, song.name + " - " + song.author + "." + song.extension)
    print("Downloaded")
    return HttpResponseRedirect(request.GET.get('return_url'))


@login_required()
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
            print (my_file.content_type)
            extension = my_file.name.rsplit('.', 1)[1]
            user = User.objects.get(pk=request.session['user_id'])
            if not user.is_superuser:                           # if normal user, upload to their own directory
                if user.profile.drive_folder_id:
                    folder_id = user.profile.drive_folder_id
                else:
                    folder_id = createFolder(user.username)
                    user.profile.drive_folder_id = folder_id
                    user.profile.save()
            else:                                       # if superuser upload to shiro store directory
                folder_id = drive_api.shiro_store_folder_id
            file_id = uploadFile(name + " - " + author + "." + extension, my_file.temporary_file_path(), my_file.content_type, folder_id=folder_id)

            new_song = Song(id=file_id, name=name, author=author, extension=extension, price=price)
            if not user.is_superuser:
                new_song.owner = user
                user.profile.songs.add(new_song)
                user.profile.save()
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
            messages.success(request, 'Register new account succeeded!')
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'sites/signup.html', {'form':form})


@login_required()
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


@login_required()
def info(request, username):
    if username != request.session['username']:
        return redirect('info', username=request.session['username'])
    print("User info: ")
    user = User.objects.get(username=username)
    print(user.profile)
    list_songs_id = [song['id'] for song in user.profile.songs.values()]
    print(list_songs_id)
    # songs = Song.objects.get(id__contains=[list_songs_id])
    # query = reduce(operator.and_, (Q(id__contains=item) for item in list_songs_id))
    # songs = Song.objects.filter(query)
    songs = user.profile.songs.all

    return render(request, 'sites/info.html', {'user': user, 'songs': songs})