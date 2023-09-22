from model.allocations import solve
from model.layout import *

allocations = solve().allocations
layout = make_layout(allocations)
roads = make_roads()

opt_result = anneal(layout)

print(opt_result)