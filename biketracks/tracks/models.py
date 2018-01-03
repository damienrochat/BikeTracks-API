from django.contrib.gis.db import models
from django.contrib.gis.measure import D
from django.db.models import QuerySet, F, Count


class TrackQuerySet(QuerySet):

    def in_radius(self, point, radius, use_centroid=True):
        """
        QuerySet of all tracks in the area,
        defined by a geo point and a radius (in meters).

        Computation based on centroid by default for better performances.
        """
        if use_centroid:
            return self.filter(centroid__distance_lte=(point, D(m=radius)))
        else:
            return self.filter(track__distance_lte=(point, D(m=radius)))


class Track(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    track = models.LineStringField(srid=4326)
    centroid = models.PointField()
    distance = models.IntegerField()
    climb = models.IntegerField()
    descent = models.IntegerField()

    objects = TrackQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.centroid = self.track.centroid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tracks'


class TrackPoint(models.Model):
    track = models.ForeignKey(Track, related_name='points', on_delete=models.CASCADE)
    pid = models.IntegerField()
    point = models.PointField(geography=True, srid=4326)
    elev = models.FloatField()

    class Meta:
        db_table = 'track_points'
        ordering = ['pid']
