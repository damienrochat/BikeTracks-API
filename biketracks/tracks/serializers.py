from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from biketracks.tracks.models import Track, TrackPoint


class TrackPointSerializer(ModelSerializer):
    lng = SerializerMethodField()
    lat = SerializerMethodField()

    def get_lng(self, obj):
        return obj.point.y

    def get_lat(self, obj):
        return obj.point.x

    class Meta:
        model = TrackPoint
        fields = ('lng', 'lat', 'elev')


class TrackSerializer(ModelSerializer):
    points = TrackPointSerializer(many=True)

    class Meta:
        model = Track
        exclude = ('track',)
