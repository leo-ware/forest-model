from model.roads import RoadNetwork
from model.constants import N

import random
import heapq as hq
import numpy as np
from tqdm import tqdm

def flood_fill(wx, wy, shape=(N, N)):
    grid = np.zeros(shape)
    grid.fill(float("inf"))
    grid[wx, wy] = 0

    queue = [(0, el) for el in zip(wx, wy)]
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        dist, (x, y) = hq.heappop(queue)
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx, ny] > dist + 1:
                grid[nx, ny] = dist + 1
                hq.heappush(queue, (dist + 1, (nx, ny)))
    
    return grid

def score_roads(layout, wx, wy):
    grid = flood_fill(wx, wy)
    return -np.sum((3 - layout) * grid)

def swap(wx, wy):
    wx = wx.copy()
    wy = wy.copy()
    i = random.randint(0, len(wx) - 1)
    nx, ny = np.random.randint(0, N, 2)
    wx[i], wy[i] = nx, ny
    return wx, wy

def anneal_roads(layout, k, iters=100, gamma=0.95):
    wx = np.random.randint(0, len(layout), k)
    wy = np.random.randint(0, len(layout[0]), k)

    best_wx = wx
    best_wy = wy
    score = best_score = score_roads(layout, wx, wy)

    temp = 1
    for _ in tqdm(range(iters)):
        nx, ny = swap(wx, wy)
        new_score = score_roads(layout, nx, ny)

        if new_score > score or random.random() < temp:
            wx, wy = nx, ny
            score = new_score
            if new_score > best_score:
                best_wx, best_wy = nx, ny
                best_score = new_score
        
        temp *= gamma
    
    return best_wx, best_wy

def make_roads(layout, k=10, max_iters=100):
    wx, wy = anneal_roads(layout, k, iters=max_iters)

    rn = RoadNetwork()
    for x, y in zip(wx, wy):
        rn.add_waypoint(x, y)
    roads = rn.layout()
    return roads
