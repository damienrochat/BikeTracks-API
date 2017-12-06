from itertools import islice

import gpxpy
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.geos import Point, LineString
from django.core.management import BaseCommand

from biketracks.tracks.models import Track


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

                    track_points = [
                        Point(x=pt.longitude, y=pt.latitude, z=pt.elevation)
                        for pt in islice(segment.points, 0, None, 1)
                    ]
                    track = LineString(track_points, srid=4326)

                    climb = 0
                    descent = 0
                    elevation_points = list(islice(track_points, 0, None, 60))
                    if len(track_points) % 60 != 0:
                       elevation_points.append(track_points[-1])

                    for i in range(1, len(elevation_points)):
                        delta = elevation_points[i].z - elevation_points[i-1].z
                        if delta > 0:
                            climb = climb + delta
                        elif delta < 0:
                            descent = descent + delta

                    Track.objects.create(
                        name=track.name,
                        type=track.type,
                        track=track,
                        distance=track.transform(ct, clone=True).length,  # distance based on ETRS89 grid
                        climb=climb,
                        descent=descent,
                    )
