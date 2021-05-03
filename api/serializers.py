from rest_framework import serializers
from .models  import Artist, Album, Track
#from .models  import Album, Track

class ArtistSerializer(serializers.Serializer):

    name = serializers.CharField(max_length = 100)
    age = serializers.IntegerField(default=0)
    #albums = serializers.URLField(max_length=200)
    #tracks = serializers.URLField(max_length=200)

class AlbumSerializer(serializers.Serializer):

    name = serializers.CharField(max_length = 100)
    genre = serializers.CharField(max_length=100)
    #artist = serializers.URLField(max_length=200)
    #tracks = serializers.URLField(max_length=200)

class TrackSerializer(serializers.Serializer):

    name = serializers.CharField(max_length = 100)
    duration = serializers.FloatField(default=0)
#    times_played = serializers.IntegerField(default=0)
#    artist = serializers.URLField(max_length=200)
#    album = serializers.URLField(max_length=200)
