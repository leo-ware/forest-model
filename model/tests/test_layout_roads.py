from model.allocations import solve
from model.layout import make_layout
from model.layout_roads import make_roads

def test_make_roads():
    layout = make_layout(solve().allocations)
    make_roads(layout, max_iters=4)
