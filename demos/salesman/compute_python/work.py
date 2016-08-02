#!/usr/bin/env python3
import copy
import math
import random
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def route_length(route):
    start_point = route[0]
    total_length = 0
    for end_point in route[1:]:
        segment_length = check_distance(start_point, end_point)
        total_length += segment_length
    total_length += check_distance(route[-1], route[0])
    return total_length

def check_distance(point1, point2):
    delta_x = point1.x - point2.x
    delta_y = point1.y - point2.y
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return distance

def new_point(max_coordinates):
    p = Point(
        random.randrange(max_coordinates),
        random.randrange(max_coordinates)
    )
    return p

def generate_points(
        amount=30,
        max_coordinates=500,
        min_distance=10
    ):
    points = []
    points.append(new_point(max_coordinates))
    while amount:
        p = new_point(max_coordinates)
        if all(check_distance(p, point) > min_distance
            for point in points):
            points.append(p)
            amount -= 1
    return points

def create_points_index(points):
    # since the points are generated randomly initially anyways,
    # we don't need the initial index to contain additional randomness
    # so all we really return here is an array which contains the indices of
    # all the points in ascending order
    return list(range(len(points)));

def copy_list(list):
    return list(list)

def swap_two(route):
    # does not ensure that two different positions are picked
    position1 = random.randrange(len(route))
    position2 = random.randrange(len(route))
    value1 = route[position1]
    route[position1] = route[position2]
    route[position2] = value1
    return route

def compute_tsp(**kwargs):
    print("compute_tsp called")

    points = kwargs["points"]
    start_route = kwargs["startRoute"]
    current_best_route = kwargs["currentBestRoute"]
    current_route = kwargs["currentRouter"]
    temp = kwargs["temperature"]
    iterations = kwargs["iterations"]

    for i in range(iterations):
        current_length = route_length(points, current_route)
        current_best_length = route_length(points, current_best_route)

        # if current_length < current_best_length) or 

def find_best_route(route=None):
    if not route:
        route = generate_points()

points = generate_points()
print(points)
print(route_length(points))
