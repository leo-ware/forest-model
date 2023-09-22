from model.constants import EFFECTIVE_INTEREST_RATE

discount_factor = 1/(1 + EFFECTIVE_INTEREST_RATE)

class PlantingStrategy:
    def __init__(self, name, yield_per_hectare, cost_per_m3, years_to_harvest, plantation_shape, horizon=500):
        self.name = name
        self.yield_per_hectare = yield_per_hectare
        self.cost_per_m3 = cost_per_m3
        self.years_to_harvest = years_to_harvest
        self.plantation_shape = plantation_shape
        self.plantation_area = plantation_shape[0] * plantation_shape[1]
    
        self.annual_revenue_per_ha = self.yield_per_hectare * self.cost_per_m3 * (1/self.years_to_harvest)
        self.present_value = sum(self.annual_revenue_per_ha * discount_factor**i for i in range(horizon))
        self.annual_yield_per_ha = self.yield_per_hectare / self.years_to_harvest

E25 = PlantingStrategy(
    name="Eucalyptus 25",
    yield_per_hectare=500,
    cost_per_m3=25,
    years_to_harvest=25,
    plantation_shape=(1, 5)
)

M100 = PlantingStrategy(
    name="Mahogany 100",
    yield_per_hectare=500,
    cost_per_m3=1300,
    years_to_harvest=100,
    plantation_shape=(0.5, 2),
)

M200 = PlantingStrategy(
    name="Mahogany 200",
    yield_per_hectare=800,
    cost_per_m3=1300,
    years_to_harvest=200,
    plantation_shape=(0.5, 2),
)

Reserve = PlantingStrategy(
    name="Reserve",
    yield_per_hectare=0,
    cost_per_m3=0,
    years_to_harvest=float("inf"),
    plantation_shape=(1, 1),
)

planting_strategies = [E25, M100, M200, Reserve]