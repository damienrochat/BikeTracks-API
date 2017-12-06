# BikeTracks API

## Before starting

This project use GeoDjango, you need a spacial database installer before starting (tested with PostgreSQL + PostGIS).

You can easily create a Docker container with the following command :

```shell
docker run --name biketracks-db -p 5432:5432 -e POSTGRES_PASSWORD=hodor -d mdillon/postgis
```

Then, install pip requirements and set local settings by creating ```biketracks/local_settings.py``` file.

During development, Django can be run with ```python manage.py runserver```.

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
    "id": 5,
    "track": [
      {
        "lng": 6.74366133,
        "lat": 46.78888733,
        "elev": 449.0
      },
      {
        "lng": 6.74366133,
        "lat": 46.78888733,
        "elev": 449.0
      }
    ],
    "name": "Vallons des Vaux",
    "type": "Xcountry",
    "distance": 8715,
    "climb": 654,
    "descent": -660
  }
]
```

