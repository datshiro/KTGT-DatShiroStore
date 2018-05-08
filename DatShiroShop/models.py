from django.db import models


# Create your models here.
class Song(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    link = models.CharField(null=True, blank=True, max_length=200)
    author = models.CharField(null=True, blank=True, max_length=100)
    price = models.FloatField(default=0)

    def __str__(self):
        if self.author is None:
            self.author = " "
        return self.name + " - " + self.author

    def save(self, *args, **kargs):
        if self.link is None:
            self.link = "https://docs.google.com/uc?export=open&id="+self.id
        super(Song,self).save(*args, **kargs)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name + " - " + self.email
