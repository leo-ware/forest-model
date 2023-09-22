import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from scipy.signal import fftconvolve

from model.layout_roads import flood_fill
from model.constants import N

def fire_avg_interarrival(dist):
    return 18*np.log(dist)

def fire_sim(G=N):
    start_chance = 1/(3*fire_avg_interarrival(100))
    spread_chance = 1/np.e

    edges_x = np.array([0]*G + [G-1]*G + list(range(G)) + list(range(G)))
    edges_y = np.array(list(range(G)) + list(range(G)) + [0]*G + [G-1]*G)

    fire_init = np.random.random(size=G*4) < start_chance
    wx = edges_x[fire_init]
    wy = edges_y[fire_init]

    fire_state = np.zeros((G, G))
    fire_state[wx, wy] = True
    dist = flood_fill(wx, wy, shape=(G, G))

    neighborhood = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])
    
    for d in sorted(np.unique(dist).astype(int)):
        if not d:
            continue

        fire_neighbors = (fftconvolve(fire_state, neighborhood, mode='same').astype(int) > 0).astype(int)
        cx, cy = np.where((dist == d) & fire_neighbors)
        spread = np.random.random(size=len(cx)) < spread_chance
        if not np.any(spread):
            break
        fire_state[cx[spread], cy[spread]] = 1
    
    return fire_state.astype(int)

    # plt.imshow(fire_state)
    # plt.colorbar()


def plot_interarrival():
    x = np.linspace(30, 3000, 100)
    plt.figure(figsize=(4, 2))
    plt.plot(x, fire_avg_interarrival(x))

    plt.ylabel('Avg Time (years)')
    plt.xlabel('Distance from forest edge (m)')
    plt.title('Average Fire Interarrival Times')
    plt.show()

def plot_log_risk():
    d1 = np.vstack([np.arange(0, N) for _ in range(N)])
    dist = d1.copy()
    for i in range(1, 4):
        dist = np.minimum(dist, np.rot90(d1, i))

    annual_fire_risk = 1/fire_avg_interarrival(dist * 100)

    plt.figure(figsize=(4, 3))
    plt.contourf(np.log(annual_fire_risk), cmap="Reds", levels=100)
    plt.axis("off")
    plt.title("Annual Risk of Fire ($\log P$)")
    plt.colorbar()
    plt.show()