from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path(r'', views.home, name='homepage'),
    path(r'download/<song_id>', views.download, name='download'),
    path(r'upload', views.upload, name='upload'),
    path(r'signup', views.signup, name='signup'),
    path(r'buy/<song_id>', views.buy_song, name='buy_song'),
    path(r'info/<username>', views.info, name='info'),
    path(r'signature/<song_id>', views.get_signature, name='signature'),
]
