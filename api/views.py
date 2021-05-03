from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import serializers
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from .models import Artist, Album, Track
from base64 import b64encode

# Create your views here.
class ArtistView(APIView):
    
    serializer_class = serializers.ArtistSerializer 

    def get(self, request, format=None):
        artists_data = list(Artist.objects.values())
        return Response(artists_data)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            age = serializer.validated_data.get('age')
            #albums = serializer.validated_data.get('albums')
            #tracks = serializer.validated_data.get('tracks')
            try:
                exists = Artist.objects.get(name=name)
                return Response({'Error': 'Artista ya existe'}, status=status.HTTP_409_CONFLICT)
            except:
                artist_new = Artist()
                artist_new.name = name
                coded_id = b64encode(name.encode()).decode('utf-8')
                artist_new.id = coded_id[:22]
                artist_new.age = age
                artist_new.albums = f'https://apit2rr4.herokuapp.com/artists/{artist_new.id}/albums'
                artist_new.tracks = f'https://apit2rr4.herokuapp.com/artists/{artist_new.id}/tracks'
                artist_new.self = f'https://apit2rr4.herokuapp.com/artists/{artist_new.id}'
                artist_new.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        return Response({'method': 'PUT'})


class ArtistIDView(APIView):

    serializer_class = serializers.ArtistSerializer

    def get(self, request, pk):
        try:
            artist_exists = Artist.objects.get(id=pk)
        except:
            return Response({'Error': 'Artista no existe'}, status=status.HTTP_404_NOT_FOUND)
        artist_data = Artist.objects.get(id=pk)
        serialized_data = ArtistSerializer(artist_data)
        dict_data = dict(serialized_data.data)
        aux_dict = dict()
        aux_dict["id"] = artist_data.id
        aux_dict["name"] = dict_data["name"]
        aux_dict["age"] = dict_data["age"]
        aux_dict["albums"] = artist_data.albums
        aux_dict["tracks"] = artist_data.tracks
        aux_dict["self"] = f'https://apit2rr4.herokuapp.com/artists/{artist_data.id}'
        return Response(aux_dict)

    def delete(self, request, pk):
        artist_data = Artist.objects.get(id=pk)
        operation = artist_data.delete()
        if operation:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumsArtistView(APIView):
    
    serializer_class = serializers.AlbumSerializer
    
    def get(self, request, pk):
        try:
            artist_exists = Artist.objects.get(id=pk)
        except:
            return Response({'Error': 'Artista no existe'}, status=status.HTTP_404_NOT_FOUND)

        albums = []
        aid = Artist.objects.get(id=pk)
        album_data = Album.objects.filter(artist_id=pk)
        for album in album_data:
            album_serialized = AlbumSerializer(album)
            album_serialized_2 = dict(album_serialized.data)
            aux_dict = dict()
            aux_dict["id"] = album.id
            aux_dict["artist_id"] = album.artist_id_id
            aux_dict["name"] = album_serialized_2["name"]
            aux_dict["genre"] = album_serialized_2["genre"]
            aux_dict["artist"] = album.artist
            aux_dict["tracks"] = album.tracks
            aux_dict["self"] = f'https://apit2rr4.herokuapp.com/albums/{album.id}'
            
            albums.append(aux_dict)
        return Response(albums)

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            genre = serializer.validated_data.get('genre')
            #artist = serializer.validated_data.get('artist')
            try:
                artist_exists = Artist.objects.get(id=pk)
            except:
                return Responde({'Error': 'Artista no existe'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                exists = Album.objects.get(name=name)
                return Response({'Error': 'Album ya existe'}, status=status.HTTP_409_CONFLICT)
            except:
                album_new = Album()
                album_new.name = name
                #coded_id = b64encode(name.encode()).decode('utf-8')
                #album_new.id = coded_id[:22]
                album_new.artist_id = Artist.objects.get(id=pk)
                artist = Artist.objects.get(id=pk)
                #album_new.artist_id = artist.id
                aux = str(album_new.artist_id)
                nom_cod = str(name)+":"+str(artist.id)
                coded_id = b64encode(nom_cod.encode()).decode('utf-8')
                album_new.id = coded_id[:22]
                album_new.genre = genre
                album_new.tracks = f'https://apit2rr4.herokuapp.com/albums/{album_new.id}/tracks'
                album_new.artist = f'https://apit2rr4.herokuapp.com/artists/{artist.id}'
                album_new.self = f'https://apit2rr4.herokuapp.com/albums/{album_new.id}'
                album_new.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# -------------------
#     Vistas Album 
# -------------------

class AlbumView(APIView):
    
    serializer_class = serializers.AlbumSerializer 

    def get(self, request, format=None):
        album_data = list(Album.objects.values())
        return Response(album_data)
    
class AlbumIDView(APIView):

    serializer_class = serializers.AlbumSerializer
    #serializer_class_2 = serializers.AlbumSerializer

    def get(self, request, pk):
        try:
            album_exists = Album.objects.get(id=pk)
        except:
            return Response({'Error': 'Album no existe'}, status=status.HTTP_404_NOT_FOUND)

        album_data = Album.objects.get(id=pk)
        serialized_data = AlbumSerializer(album_data)
        dict_data = dict(serialized_data.data)
        aux_dict = dict()
        aux_dict["id"] = album_data.id
        aux_dict["artist_id"] = album_data.artist_id_id
        aux_dict["name"] = dict_data["name"]
        aux_dict["genre"] = dict_data["genre"]
        aux_dict["artist"] = album_data.artist
        aux_dict["tracks"] = album_data.tracks
        aux_dict["self"] = f'https://apit2rr4.herokuapp.com/albums/{album_data.id}'
        #dict_data["id"] = album_data.id
        #dict_data["artist"] = album_data.artist
        #dict_data["tracks"] = album_data.tracks
        #return Response(dict_data)
        return Response(aux_dict)

    def delete(self, request, pk):
        album_data = Album.objects.get(id=pk)
        operation = album_data.delete()
        if operation:
            return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------
#     Vistas Track 
# -------------------

class TrackView(APIView):
    serializer_class = serializers.TrackSerializer 

    def get(self, request, format=None):
        track_data = list(Track.objects.values())
        return Response(track_data)

class TracksAlbumView(APIView):
    serializer_class = serializers.TrackSerializer
    
    def get(self, request, pk):
        try:
            album_exists = Album.objects.get(id=pk)
        except:
            return Response({'Error': 'Album no existe'}, status=status.HTTP_404_NOT_FOUND)

        tracks = []
        aid = Album.objects.get(id=pk)
        track_data = Track.objects.filter(album_id=pk)
        for track in track_data:
            track_serialized = TrackSerializer(track)
            track_serialized_2 = dict(track_serialized.data)
            aux_dict = dict()
            aux_dict["id"] = track.id
            aux_dict["album_id"] = track.album_id_id
            aux_dict["name"] = track_serialized_2["name"]
            aux_dict["duration"] = track_serialized_2["duration"]
            aux_dict["times_played"] = track.times_played
            aux_dict["artist"] = track.artist
            aux_dict["album"] = track.album
            aux_dict["self"] = f'https://apit2rr4.herokuapp.com/tracks/{track.id}'

            tracks.append(aux_dict)
        return Response(tracks)

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            duration = serializer.validated_data.get('duration')
            #artist = serializer.validated_data.get('artist')
            try:
                album_exists = Album.objects.get(id=pk)
            except:
                return Responde({'Error': 'Album no existe'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            try:
                exists = Track.objects.get(name=name)
                return Response({'Error': 'Cancion ya existe'}, status=status.HTTP_409_CONFLICT)
            except:
                track_new = Track()
                track_new.name = name
                track_new.album_id = Album.objects.get(id=pk)
                album = Album.objects.get(id=pk)
                aux = album.artist_id
                aux_id = aux.id 
                nom_cod = str(name)+":"+str(album.id)
                coded_id = b64encode(nom_cod.encode()).decode('utf-8')
                track_new.id = coded_id[:22]
                track_new.duration = duration
                track_new.artist = f'https://apit2rr4.herokuapp.com/artists/{aux_id}'
                track_new.album = f'https://apit2rr4.herokuapp.com/albums/{album.id}'
                track_new.self = f'https://apit2rr4.herokuapp.com/tracks/{track_new.id}'
                track_new.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                #return Response(aux_dict, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class TracksArtistView(APIView):
    serializer_class = serializers.TrackSerializer
    
    def get(self, request, pk):
        try:
            artist_exists = Artist.objects.get(id=pk)
        except:
            return Response({'Error': 'Artista no existe'}, status=status.HTTP_404_NOT_FOUND)

        albums = []
        #aid = Artist.objects.get(id=pk)
        #alb_id = Album.objects.get(artist_id=pk)
        albums_data = Album.objects.filter(artist_id=pk)
        for album in albums_data:
            album_serialized = AlbumSerializer(album)
            album_serialized_2 = dict(album_serialized.data)
            aux_dict = dict()
            aux_dict["id"] = album.id
            aux_dict["artist_id"] = album.artist_id_id
            aux_dict["name"] = album_serialized_2["name"]
            aux_dict["genre"] = album_serialized_2["genre"]
            aux_dict["artist"] = album.artist
            aux_dict["tracks"] = album.tracks
            aux_dict["self"] = f'https://apit2rr4.herokuapp.com/albums/{album.id}'
            albums.append(aux_dict)
            
        tracks = []
        for element in albums:
            aux_id = element['id']
            track_data = Track.objects.filter(album_id=aux_id)
            for track in track_data:
                track_serialized = TrackSerializer(track)
                track_serialized_2 = dict(track_serialized.data)
                aux_dict_2 = dict()
                aux_dict_2["album_id"] = track.album_id_id
                aux_dict_2["id"] = track.id
                aux_dict_2["name"] = track_serialized_2["name"]
                aux_dict_2["duration"] = track_serialized_2["duration"]
                aux_dict_2["times_played"] = track.times_played
                aux_dict_2["artist"] = track.artist
                aux_dict_2["album"] = track.album
                aux_dict_2["self"] = f'https://apit2rr4.herokuapp.com/tracks/{track.id}'

                tracks.append(aux_dict_2)
                #tracks.append(track_serialized_2)
        return Response(tracks)

class TrackIDView(APIView):
    serializer_class = serializers.TrackSerializer

    def get(self, request, pk):
        try:
            track_exists = Track.objects.get(id=pk)
        except:
            return Response({'Error': 'Cancion no existe'}, status=status.HTTP_404_NOT_FOUND)
        track_data = Track.objects.get(id=pk)
        serialized_data = TrackSerializer(track_data)
        dict_data = dict(serialized_data.data)
        aux_dict = dict()
        aux_dict["id"] = track_data.id
        aux_dict["album_id"] = track_data.album_id_id
        aux_dict["name"] = dict_data["name"]
        aux_dict["duration"] = dict_data["duration"]
        aux_dict["times_played"] = track_data.times_played
        aux_dict["artist"] = track_data.artist
        aux_dict["album"] = track_data.album
        aux_dict["self"] = f'https://apit2rr4.herokuapp.com/tracks/{track_data.id}'
        return Response(aux_dict)

    def delete(self, request, pk):
        track_data = Track.objects.get(id=pk)
        operation = track_data.delete()
        if operation:
            return Response(status=status.HTTP_204_NO_CONTENT)
