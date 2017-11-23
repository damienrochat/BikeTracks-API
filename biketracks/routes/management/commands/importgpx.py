import gpxpy
from django.contrib.gis.geos import Point, LineString
from django.core.management import BaseCommand

from routes.models import Route


class Command(BaseCommand):
    help = 'Import all GPX files from data directory'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['files']:
            gpx = gpxpy.parse(open(filename))

            for track in gpx.tracks:
                for segment in track.segments:
                    Route.objects.create(
                        name=track.name,
                        type=track.type,
                        route=LineString([
                            Point(x=point.longitude, y=point.latitude, z=point.elevation)
                            for point in segment.points
                        ], srid=4326)
                    )
