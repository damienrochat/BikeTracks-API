import gpxpy
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.geos import Point, LineString
from django.core.management import BaseCommand

from routes.models import Route


class Command(BaseCommand):
    help = 'Import GPX files'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        ct = CoordTransform(SpatialReference(4326), SpatialReference(3035))  # transform wgs84 to european grid

        for filename in options['files']:
            gpx = gpxpy.parse(open(filename))

            for track in gpx.tracks:
                for segment in track.segments:
                    climb = 0
                    descent = 0

                    for i in range(1, len(segment.points)):
                        delta = segment.points[i].elevation - segment.points[i-1].elevation
                        if delta > 0:
                            climb = climb + delta
                        elif delta < 0:
                            descent = descent + delta

                    route = LineString([
                        Point(x=point.longitude, y=point.latitude, z=point.elevation)
                        for point in segment.points
                    ], srid=4326)

                    Route.objects.create(
                        name=track.name,
                        type=track.type,
                        route=route,
                        distance=route.transform(ct, clone=True).length,  # distance based on ETRS89 grid
                        climb=climb,
                        descent=descent,
                    )
