from django.conf.urls import url

from biketracks.tracks.views import TracksView

urlpatterns = [
    url(r'^$', TracksView.as_view(), name='tracks'),
]
