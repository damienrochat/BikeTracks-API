from rest_framework.fields import FloatField
from rest_framework.serializers import ModelSerializer, Serializer

from routes.models import Route


class RoutePointSerializer(Serializer):
    lat = FloatField(required=True)
    lng = FloatField(required=True)

    def to_representation(self, instance):
        return dict(lat=instance[1], lng=instance[0])


class RouteSerializer(ModelSerializer):
    route = RoutePointSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'
