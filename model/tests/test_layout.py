from model.allocations import solve
from model.layout import *

def test_runs():
    allocations = solve().allocations
    layout = make_layout(allocations)
    # roads = make_roads()
    plot_map(layout)

# def test_anneal():
#     allocations = solve().allocations
#     layout = make_layout(allocations)
#     opt_result = anneal(layout, max_iters=10)