import random
import numpy as np

from model.constants import MILL_LOCATION

class RoadNetwork:
    def __init__(self, width=173, height=173, mill_location=MILL_LOCATION):
        self.width = width
        self.height = height
        self.mill_location = mill_location
        self.waypoints = {mill_location}
    
    def add_waypoint(self, x, y):
        self.waypoints.add((x, y))
    
    def delete_waypoint(self, x, y):
        self.waypoints.remove((x, y))
    
    def pave(self, origin, dest, roads):
        x, y = origin

        if dest[0] > origin[0]:
            x_dir = 1
        elif dest[0] < origin[0]:
            x_dir = -1
        else:
            x_dir = 0
        
        if dest[1] > origin[1]:
            y_dir = 1
        elif dest[1] < origin[1]:
            y_dir = -1
        else:
            y_dir = 0

        while x != dest[0] or y != dest[1]:
            if y == dest[1]:
                y_dir = 0
            if x == dest[0]:
                x_dir = 0

            if y_dir and (0 <= y + y_dir < self.height) and roads[x, y + y_dir]:
                y += y_dir
                continue
            if x_dir and (0 <= x + x_dir < self.width) and roads[x + x_dir, y]:
                x += x_dir
                continue

            y_dist = abs(dest[1] - y)
            x_dist = abs(dest[0] - x)
            if random.random() < y_dist/(x_dist + y_dist):
                y += y_dir
            else:
                x += x_dir
            roads[x, y] = 1

        return roads

    
    def layout(self):
        roads = np.zeros((self.height, self.width))
        roads[self.mill_location[0], self.mill_location[1]] = 1
        
        for x, y in self.waypoints:
            if not roads[x, y]:
                roads = self.pave(self.mill_location, (x, y), roads)

        self.pave(self.mill_location, (self.mill_location[0], self.height - 1), roads)
        
        return roads

