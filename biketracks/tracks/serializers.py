from rest_framework.serializers import ModelSerializer, Serializer

from tracks.models import Track


class TrackPointSerializer(Serializer):

    def to_representation(self, instance):
        return dict(lng=instance[0], lat=instance[1], elev=instance[2])


class TrackSerializer(ModelSerializer):
    track = TrackPointSerializer(many=True)

    class Meta:
        model = Track
        fields = '__all__'
