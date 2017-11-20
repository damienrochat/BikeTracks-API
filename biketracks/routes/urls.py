from django.conf.urls import url

from routes.views import RoutesView

urlpatterns = [
    url(r'^$', RoutesView.as_view(), name='routes'),
]
