from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.db.models import QuerySet


class TrackQuerySet(QuerySet):

    def in_radius(self, point, radius):
        """
        QuerySet of all tracks in the area,
        defined by a geo point and a radius (in meters).
        """
        return self.filter(track__distance_lte=(point, D(m=radius)))


class Track(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    track = models.LineStringField(srid=4326)
    distance = models.IntegerField()
    climb = models.IntegerField()
    descent = models.IntegerField()

    objects = TrackQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tracks'


class TrackPoint(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.IntegerField()
    point = models.PointField(geography=True, srid=4326)
    elev = models.FloatField()

    class Meta:
        db_table = 'track_points'
