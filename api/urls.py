from django.urls import path
from api import views

urlpatterns = [
    path('artists/', views.ArtistView.as_view()),
    path('artists/<str:pk>', views.ArtistIDView.as_view()),
    path('artists/<str:pk>/albums', views.AlbumsArtistView.as_view()),
    path('artists/<str:pk>/tracks', views.TracksArtistView.as_view()),
    path('albums/', views.AlbumView.as_view()),
    path('albums/<str:pk>', views.AlbumIDView.as_view()),
    path('albums/<str:pk>/tracks', views.TracksAlbumView.as_view()),
    path('tracks/', views.TrackView.as_view()),
    path('tracks/<str:pk>', views.TrackIDView.as_view()),
]
