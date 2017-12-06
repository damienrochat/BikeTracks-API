from itertools import islice


def compute_elevation(points, interval=60):
    climb = 0
    descent = 0

    elevation_points = list(islice(points, 0, None, interval))

    if len(points) % interval is not 0:
        elevation_points.append(points[-1])

    for i in range(1, len(elevation_points)):
        delta = elevation_points[i]['elev'] - elevation_points[i - 1]['elev']
        if delta > 0:
            climb = climb + delta
        elif delta < 0:
            descent = descent - delta

    return climb, descent
