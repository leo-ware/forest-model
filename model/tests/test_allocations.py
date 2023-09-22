from model.allocations import *

def test_for_individual_plantations():
    allocations = {s.name: p for s, p in zip(planting_strategies, n_plantations)}
    strategies = {s.name: s for s in planting_strategies}
    reset()
    
    assert avg_annual_revenue.value == 0
    assert habitats() == 0
    assert total_yield.value == 0
    assert total_plantation_size.value == 0
    
    for name in strategies.keys():
        reset()
        allocations[name].value = 1

        assert avg_annual_revenue.value == (
            strategies[name].annual_revenue_per_ha *
            strategies[name].plantation_area
            ), f"Failed for {name}"
        assert habitats() == 0, f"Failed for {name}"
        assert total_yield.value == (
            strategies[name].annual_yield_per_ha *
            strategies[name].plantation_area
            ), f"Failed for {name}"
        assert total_plantation_size.value == strategies[name].plantation_area,\
            f"Failed for {name}"
    
def test_habitat_calcs():
    reset()
    allocations = {s.name: p for s, p in zip(planting_strategies, n_plantations)}
    strategies = {s.name: s for s in planting_strategies}

    allocations["Mahogany 200"].value = 500
    
    assert floor(breeding_forest.value) == 125 # 500*(1 - 150/200)
    assert floor(roaming_forest.value) == 312 # 500*(1 - 80/200)
    assert habitats() == 1

def test_solve():
    solve()

def test_max_parrots():
    max_parrots(0)
    max_parrots()