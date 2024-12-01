import math
from typing import Tuple, Union


def distance_between(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


def get_midpoint(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def calc_normal_line(p1, p2):
    """Normal line is the lane perpendicular to the tangent at a given point along a line."""
    # How long the normal line should be // TODO: Return point and angle instead?
    scale = 100
    x1, y1 = p1
    x2, y2 = p2

    # Find midpoint
    midpoint = get_midpoint(p1, p2)

    # Find slope of the normal line (perpendicular to original line segment)
    delta_x = x2 - x1
    delta_y = y2 - y1
    slope = (delta_y, -1 * delta_x)

    # Scale the vector to normalize the size of the line
    mag = math.sqrt(math.pow(slope[0], 2) + math.pow(slope[1], 2))
    scale_vector = ((slope[0] / mag) * scale, (slope[1] / mag) * scale)

    # Offset the second point from midpoint using the scaled vector
    second_point = (midpoint[0] + scale_vector[0], midpoint[1] + scale_vector[1])
    return [midpoint, second_point]


# MINIMUM_DISTANCE = 50
MINIMUM_DISTANCE = 10


def upsample_line(points):
    new_points = [points[0]]
    for index in range(0, len(points) - 1):
        second_index = (index + 1) % (len(points) - 1)
        prospective_point = points[second_index]
        while distance_between(new_points[-1], points[second_index]) > MINIMUM_DISTANCE:
            if distance_between(new_points[-1], prospective_point) > MINIMUM_DISTANCE:
                prospective_point = get_midpoint(new_points[-1], prospective_point)
            else:
                new_points.append(prospective_point)
                prospective_point = points[second_index]
        new_points.append(points[second_index])
    return new_points


def points_to_vector(p1, p2):
    delta_x = p2[0] - p1[0]
    delta_y = p2[1] - p1[1]
    return (delta_y, -1 * delta_x)


def points_to_angle(first, mid, last):
    v1_x, v1_y = points_to_vector(first, mid)
    v2_x, v2_y = points_to_vector(mid, last)
    mid_x, mid_y = mid

    angle = math.atan2(mid_y - v1_y, mid_x - v1_x) - math.atan2(
        mid_y - v2_y, mid_x - v2_x
    )
    print(angle)


def line_intersection(
    line1: Tuple[float, float], line2: Tuple[float, float]
) -> Union[None, Tuple[float, float]]:
    """
    Find the intersection point of two lines. If the lines are parallel, or if either is not a line
    (i.e. the points are the same) then None is returned.

    :param line1: A line segment defined by two points
    :param line2: A line segment defined by two points
    :return: A tuple of two floats representing the point of intersection, or None
    """
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
