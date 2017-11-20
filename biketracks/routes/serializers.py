from rest_framework.serializers import ModelSerializer

from routes.models import Route


class RouteSerializer(ModelSerializer):

    class Meta:
        model = Route
        fields = ('id', 'name', 'route')
