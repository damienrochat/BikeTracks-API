from django.urls import path

from biketracks.tracks.views import TracksView, TrackView

urlpatterns = [
    path('', TracksView.as_view(), name='tracks'),
    path('<int:pk>/', TrackView.as_view(), name='track'),
]
