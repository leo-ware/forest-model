from model.allocations import solve
from model.roads import RoadNetwork
from model.plot_utils import cmap, legend_content, legend_names
from model.constants import MILL_LOCATION, N

from dataclasses import dataclass
from math import floor, ceil, log
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from tqdm import tqdm

def make_layout(allocations):
    n = N

    layout = np.zeros((n, n))
    layout.fill(3)

    remain = allocations.copy()

    m = 25

    m_width = (allocations["Mahogany 100"] + allocations["Mahogany 200"]) / \
        (allocations["Mahogany 100"] + allocations["Mahogany 200"] + allocations["Eucalyptus 25"])
    m_width = floor(m_width * n)
    for x in reversed(range(n)):
        if remain["Mahogany 100"] or remain["Mahogany 200"]:
            for y in range(m_width):
                if remain["Mahogany 100"]:
                    layout[x, y] = 1
                    remain["Mahogany 100"] -= 1

                elif remain["Mahogany 200"]:
                    layout[x, y] = 2
                    remain["Mahogany 200"] -= 1

        for y in range(m_width, n):
            if remain["Eucalyptus 25"]:
                layout[x, y] = 0
                remain["Eucalyptus 25"] -= 1
    
    return layout

# def make_roads():
#     waypoints = [
#         [123, 85],
#         [23, 86],
#         [23, 66],
#         [23, 100],
#         [23, 166],
#         [150, 67],
#         [168, 160],
#     ]

#     rn = RoadNetwork()
#     for w in waypoints:
#         rn.add_waypoint(*w)
#     return rn.layout()

@dataclass
class AnnealResult:
    best: float
    best_layout: np.ndarray
    iters: int

    scores: list
    best_scores: list
    temps: list


def score(layout, e25_weight=0):
    breeding_areas = (layout == 3) + 0.25 * (layout == 2)
    roaming_areas = 0.25 * (layout == 1) + (1 - 75/200) * (layout == 2) + (layout == 3)
    bv = fftconvolve(breeding_areas, np.ones((22, 22)), mode='same') > 80
    rv = fftconvolve(roaming_areas, np.ones((22, 22)), mode='same') > 120
    parrots_est = (bv & rv).sum()

    e25_cost = e25_weight * np.where(layout == 0)[1].sum()

    return parrots_est - e25_cost


def swap_random(layout, window):
    x1 = x2 = y1 = y2 = 0
    while (
        x1 <= x2 <= x1+window or
        x2 <= x1 <= x2+window or
        y1 <= y2 <= y1+window or
        y2 <= y1 <= y2+window
    ):
        x1, x2, y1, y2 = np.random.randint(0, N - window, size=4)
    new_layout = layout.copy()
    new_layout[x1:x1+window, y1:y1+window], new_layout[x2:x2+window, y2:y2+window] = (
        layout[x2:x2+window, y2:y2+window],
        layout[x1:x1+window, y1:y1+window]
    )
    return new_layout


def anneal(layout, max_iters=10000, window_init=20, iters_per_window=5000, window_shrink=0.5, gamma=0.99, temp_init=0.5):
    assert window_shrink < 1

    window = window_init
    best_score = current_score = score(layout)
    best_layout = current_layout = layout

    iters = 0
    scores = []
    temps = []
    best_scores = []

    for _ in tqdm(range(ceil(log(window_init, 1/window_shrink)))):
        temp = temp_init
        # print(f"window_size {window}")

        for _ in range(iters_per_window):
            iters += 1
            # print("gonna swap")
            new_layout = swap_random(current_layout, window)
            # print("swapped")
            new_score = score(new_layout, e25_weight=0)
            if new_score > current_score or np.random.rand() < temp:
                current_layout = new_layout
                current_score = new_score
                if current_score > best_score:
                    best_layout = current_layout
                    best_score = current_score
            
            scores.append(current_score)
            best_scores.append(best_score)
            temps.append(temp)

            temp *= gamma
        
        if (window * window_shrink >= 1) and (iters < max_iters):
            window = int(round(window * window_shrink))
        else:
            break
    
    return AnnealResult(best_score, best_layout, iters, scores, best_scores, temps)




def plot_anneal_result(result):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    axtl = plt.subplot(2, 2, 1)
    axll = plt.subplot(2, 2, 3)
    axr = plt.subplot(1, 2, 2)

    axtl.plot(result.best_scores, label='Best', c="C1")
    axtl.plot(result.scores, label='Current', c="C0")
    
    axtl.legend(loc='lower right')
    axtl.set_ylabel('Score')
    axtl.set_xlabel('Iteration')

    axll.plot(result.temps)
    axll.set_ylabel('Temperature')
    axll.set_xlabel('Iteration')

    axr.imshow(result.best_layout)
    axr.axis('off')

    plt.tight_layout()


def plot_map(layout, roads=None, title="Recommended Concession Layout"):
    fig, ax = plt.subplots(1, 2, width_ratios=(3, 1.4), figsize=(5, 3))

    ax[1].legend(legend_content, legend_names, fontsize=8, frameon=False)
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].axis('off')

    ax[0].imshow(layout, cmap=cmap, interpolation='nearest')
    ax[0].plot(MILL_LOCATION[0], MILL_LOCATION[1], 'o', markersize=5, color='black', label='Sawmill')
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_xlabel('17.3 km')
    ax[0].set_ylabel('17.3 km', rotation=90)

    if roads is not None:
        ax[0].scatter(*np.where(roads), color='#302d2a', s=0.05)

    if title:
        fig.suptitle(title, y=0.975)
    return fig
