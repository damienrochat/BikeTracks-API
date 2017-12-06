from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from tracks.models import Track
from tracks.serializers import TrackSerializer


def safe_cast(to_type):
    def _safe_cast(val, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default
    return _safe_cast


class TracksView(ListAPIView):
    serializer_class = TrackSerializer

    # TODO: add 'limit' support
    def get_queryset(self):
        """
        Provide a custom queryset in order to list the nearest tracks.

        Filter by a lat/lng location and a radius (km, default 5).
        Almost one part of the track need to be in the area to be listed.
        Check that the request contains "lat", "lng" query string parameters,
        raise a validation error otherwise.

        The list is ordered from the nearest to farthest tracks.
        """
        to_float = safe_cast(float)
        to_int = safe_cast(int)

        lat = to_float(self.request.query_params.get('lat', None))
        lng = to_float(self.request.query_params.get('lng', None))
        if lat is None or lng is None:
            raise ValidationError('lat and lng parameters are required.')

        point = Point(lng, lat)
        radius = to_int(self.request.query_params.get('radius', 5000))

        return Track.objects.in_radius(point, radius).all()
