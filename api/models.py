from django.db import models

# Create your models here.
class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='')
    age = models.IntegerField(default=0)
    albums = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200, default='')


class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, default='')
    genre = models.CharField(max_length=50)
    artist = models.URLField(max_length=200)
    tracks = models.URLField(max_length=200)
    self = models.URLField(max_length=200, default='')


class Track(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='')
    duration = models.FloatField(default=0)
    times_played = models.IntegerField(default=0)
    artist = models.URLField(max_length=200)
    album = models.URLField(max_length=200)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    self = models.URLField(max_length=200, default='')
