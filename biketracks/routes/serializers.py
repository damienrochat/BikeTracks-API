from rest_framework.serializers import ModelSerializer, Serializer

from routes.models import Route


class RoutePointSerializer(Serializer):

    def to_representation(self, instance):
        return dict(lng=instance[0], lat=instance[1], elev=instance[2])


class RouteSerializer(ModelSerializer):
    route = RoutePointSerializer(many=True)

    class Meta:
        model = Route
        fields = '__all__'
