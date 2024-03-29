import random

import gpxpy
from django.contrib.gis.geos import Point, LineString
from django.core.management import BaseCommand

from biketracks.tracks.models import Track, TrackPoint
from biketracks.tracks.elevation import compute_elevation


def get_name(s, i=0):
    if not s:
        return 'Track {}'.format(i)
    return s


def get_type(t):
    if not t:
        return 'Xcountry'
    return t


class Command(BaseCommand):
    help = 'Import GPX files'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)
        parser.add_argument('--interval', dest='interval', type=int, default=1)

    def handle(self, *args, **options):
        for fid, filename in enumerate(options['files']):
            gpx = gpxpy.parse(open(filename))

            for track in gpx.tracks:
                for segment in track.segments:

                    # create geometric linestring (european projection ETRS89)
                    linestring = LineString([
                            Point(x=pt.longitude, y=pt.latitude, srid=4326)
                            for pt in segment.points
                        ], srid=4326)
                    linestring.transform(3035)

                    # compute positive and negative elevation
                    elev_pos, elev_neg = compute_elevation([
                        dict(
                            lng=pt.longitude,
                            lat=pt.latitude,
                            elev=pt.elevation,
                            time=pt.time,
                        )
                        for pt in segment.points
                    ], interval=options['interval'])

                    # create track
                    track = Track.objects.create(
                        name=get_name(track.name, fid),
                        type=get_type(track.type),
                        track=linestring,
                        distance=linestring.length,
                        climb=elev_pos,
                        descent=elev_neg,
                    )

                    # create each track points
                    TrackPoint.objects.bulk_create([
                        TrackPoint(
                            track=track,
                            pid=i,
                            point=Point(x=pt.longitude, y=pt.latitude, srid=4326),
                            elev=pt.elevation
                        )
                        for i, pt in enumerate(segment.points)
                    ])
