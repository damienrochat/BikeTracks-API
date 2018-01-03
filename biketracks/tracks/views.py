import math
from django.contrib.gis.geos import Point
from django.db.models import Prefetch, F
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from biketracks.tracks.models import Track, TrackPoint
from biketracks.tracks.serializers import TrackSerializer


def safe_cast(to_type):
    def _safe_cast(val, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default
    return _safe_cast


class TracksView(ListAPIView):
    serializer_class = TrackSerializer

    def _get_center(self):
        if not hasattr(self, '_center'):
            to_float = safe_cast(float)

            lat = to_float(self.request.query_params.get('lat', None))
            lng = to_float(self.request.query_params.get('lng', None))
            if lat is None or lng is None:
                raise ValidationError('lat and lng parameters are required.')

            self._center = Point(lng, lat)

        return self._center

    def _get_radius(self):
        if not hasattr(self, '_radius'):
            self._radius = safe_cast(int)(self.request.query_params.get('radius', 5000))
        return self._radius

    def _get_points_precision(self):
        if not hasattr(self, '_points_precision'):
            self._points_precision = min(10000 / self._get_radius(), 0.5)  # precision max (50%) at 10km
        return self._points_precision

    def get_queryset(self):
        """
        Provide a custom queryset in order to list the nearest tracks.

        Filter by a lat/lng location and a radius (km, default 5).
        Almost one part of the track need to be in the area to be listed.
        Check that the request contains "lat", "lng" query string parameters,
        raise a validation error otherwise.

        For a better performance, not all track points are returned from this endpoint.
        The precision is based on the radius, more wide it is, less points are returned.
        """
        interval = math.ceil(1 / self._get_points_precision())
        prefetch_queryset = TrackPoint.objects.annotate(pid_mod=F('pid') % interval).filter(pid_mod=0)

        return Track.objects\
            .in_radius(self._get_center(), self._get_radius())\
            .prefetch_related(Prefetch('points', queryset=prefetch_queryset))\
            .all()

    def get_serializer_context(self):
        context = super(TracksView, self).get_serializer_context()
        context.update({
            'points_precision': self._get_points_precision()
        })
        return context
