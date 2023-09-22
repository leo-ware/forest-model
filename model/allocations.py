import cvxpy as cp
# from cvxpy.atoms.affine import hstack
import numpy as np
from dataclasses import dataclass
from math import floor

from model.financials import planting_strategies
from model.constants import *

forest_size = N**2 - 1

n_plantations = [cp.Variable(integer=True) for _ in planting_strategies]
allocation_areas = [n_plantations[i] * planting_strategies[i].plantation_area for i in range(len(n_plantations))]

# parameters
min_habitats = cp.Parameter(nonneg=True)
min_yield = cp.Parameter(nonneg=True)

# calculations
total_plantation_size = 0
breeding_forest = 0
roaming_forest = 0
total_yield = 0
avg_annual_revenue = 0

for var, strategy, area in zip(n_plantations, planting_strategies, allocation_areas):
    portion_breeding = max(0, (1 - MIN_AGE_BREEDING/strategy.years_to_harvest))
    portion_roaming = max(0, (1 - MIN_AGE_ROAMING/strategy.years_to_harvest))

    total_plantation_size = total_plantation_size + area
    breeding_forest = breeding_forest + area * portion_breeding
    roaming_forest = roaming_forest + area * portion_roaming
    total_yield = total_yield + area * strategy.annual_yield_per_ha
    avg_annual_revenue = avg_annual_revenue + area * strategy.annual_revenue_per_ha

breeding_habitats = breeding_forest / MIN_HABITAT_BREEDING
roaming_habitats = roaming_forest / MIN_HABITAT_ROAMING

def habitats():
    return min(floor(breeding_forest.value / MIN_HABITAT_BREEDING), floor(roaming_forest.value / MIN_HABITAT_ROAMING))

# constraints
positivity_constraints = [n_plantations[i] >= 0 for i in range(len(n_plantations))]

project_constraints = [
    total_plantation_size <= forest_size,
    breeding_forest >= min_habitats * MIN_HABITAT_BREEDING,
    roaming_forest >= min_habitats * MIN_HABITAT_ROAMING,
    total_yield >= min_yield,
]

# objective
obj = cp.Maximize(avg_annual_revenue)

# solve
prob = cp.Problem(obj, project_constraints + positivity_constraints)

@dataclass(frozen=True)
class Solution:
    PARAM_min_yield: float
    PARAM_min_habitats: int
    allocations: dict

    avg_annual_revenue: float
    habitats: int
    annual_yield: float

def reset():
    for var in n_plantations:
        var.value = 0
    min_yield.value = MIN_YIELD
    min_habitats.value = MIN_HABITATS

def solve(set_min_yield=MIN_YIELD, set_min_habitats=MIN_HABITATS):
    min_yield.value = set_min_yield
    min_habitats.value = set_min_habitats
    revenue = prob.solve()

    return Solution(
        PARAM_min_yield=set_min_yield,
        PARAM_min_habitats=set_min_habitats,
        allocations={strategy.name: int(area.value) for strategy, area in zip(planting_strategies, allocation_areas)},

        avg_annual_revenue=revenue,
        habitats=habitats(),
        annual_yield=total_yield.value,
    )

def max_parrots(set_min_yield=MIN_YIELD):
    min_yield.value = set_min_yield
    obj = cp.Maximize(breeding_habitats)
    prob = cp.Problem(obj, project_constraints + positivity_constraints + [roaming_habitats >= breeding_habitats])
    return prob.solve()
