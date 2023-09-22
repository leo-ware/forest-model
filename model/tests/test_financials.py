from model.financials import *

def test_assesment():
    foo = PlantingStrategy(
        name="Foo",
        yield_per_hectare=1,
        cost_per_m3=1,
        years_to_harvest=1,
        plantation_shape=(1, 1),
    )

    assert foo.annual_revenue_per_ha == 1
    assert foo.annual_yield_per_ha == 1
    assert foo.present_value == sum(discount_factor**i for i in range(500))
    assert foo.plantation_area == 1