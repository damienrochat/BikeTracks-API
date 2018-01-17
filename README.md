# BikeTracks API

## Before starting

This project use GeoDjango, you need a spacial database installed before starting (tested with PostgreSQL 10.1 + PostGIS 2.4.2).

You can easily create a Docker container with the following command :

```shell
docker run --name biketracks-db -p 5432:5432 -e POSTGRES_PASSWORD=hodor -d mdillon/postgis
```

Then, install pip requirements and set local settings by creating ```biketracks/local_settings.py``` file.

During development, Django can be run with ```python manage.py runserver```.

## Import GPX files

You can simply add data to the database by importing .gpx files. Use the following command.

```shell
$ python manage.py importgpx /path/to/gpx/*.gpx
```

The command will extract latitude, longitude and elevation of the track points. You can optionally define the kind of track and its name.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="Creator_name">
  <trk>
    <name>Name_of_the_track</name>
    <type>Downhill|Freeride|Enduro|Xcountry</type>
    <trkseg>
      <trkpt lat="46.78888733" lon="6.74366133">
        <ele>449.0</ele>
        <time>2017-09-22T10:11:35.000Z</time>
      </trkpt>
      ...
    </trkseg>
  </trk>
</gpx>
```

Elevation computation could be affected by GPS noise.
In order to minimize it, use the optional parameter to reduce the number of points to use for it.

```shell
$ python manage.py importgpx /path/to/gpx/*.gpx --interval=60
```

## API

#### Tracks around coordinates

###### Arguments

| Argument | Optional |
| -------- | -------- |
| lat      | ✘        |
| lng      | ✘        |
| radius   | ✔        |

###### Example

```http
GET /api/v1/tracks/?lat=46.7833&lng=6.65&radius=1000
```

```http
HTTP 200 OK
Content-Type: application/json

[
  {
    "id": 42,
    "points": [
      {
        "lng": 6.75655267,
        "lat": 46.77559117,
        "elev": 584.0
      },
      {
        "lng": 6.75652383,
        "lat": 46.77561933,
        "elev": 582.0
      }
    ],
    "precision": 0.4,
    "name": "Vallons des Vaux",
    "type": "Xcountry",
    "distance": 8715,
    "climb": 654,
    "descent": 660
  }
]
```

#### Track details

###### Example

```http
GET /api/v1/tracks/42
```

```http
HTTP 200 OK
Content-Type: application/json

[
  {
    "id": 42,
    "points": [
      {
        "lng": 6.75655267,
        "lat": 46.77559117,
        "elev": 584.0
      },
      {
        "lng": 6.75652383,
        "lat": 46.77561933,
        "elev": 582.0
      }
    ],
    "name": "Vallons des Vaux",
    "type": "Xcountry",
    "distance": 8715,
    "climb": 654,
    "descent": 660
  }
]
```

