from django.conf.urls import url

from tracks.views import TracksView

urlpatterns = [
    url(r'^$', TracksView.as_view(), name='tracks'),
]
