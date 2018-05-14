from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from DatShiroShop.forms import UploadFileForm, SignUpForm
from DatShiroShop.models import Song, Profile
from api.drive_api import list_files, get_file, load_files_to_sqlite, downloadFile, uploadFile


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