from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.home, name='homepage'),
    path(r'download/<song_id>', views.download, name='download'),
    path(r'upload', views.upload, name='upload'),
]
