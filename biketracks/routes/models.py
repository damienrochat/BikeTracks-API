from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.contrib.gis.measure import D


class RouteQuerySet(GeoQuerySet):

    def in_radius(self, point, radius):
        """
        QuerySet of all routes in the area,
        defined by the geo point and the radius (in meters).

        Add and order by 'distance' attribute.
        """
        return self.filter(route__distance_lte=(point, D(m=radius))).distance(point).order_by('distance')


class Route(models.Model):
    name = models.CharField(max_length=60)
    route = models.LineStringField(geography=True, dim=3)

    objects = RouteQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'route'
