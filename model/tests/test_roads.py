from model.roads import RoadNetwork
import random

def test_runs():
    rn = RoadNetwork()
    rn.add_waypoint(10, 10)
    rn.layout()

def test_small():
    random.seed(1)
    roads = RoadNetwork(5, 5, (4, 4))
    roads.add_waypoint(0, 0)
    roads.layout()

def test_small_two():
    random.seed(1)
    roads = RoadNetwork(5, 5, (4, 4))
    roads.add_waypoint(0, 0)
    roads.add_waypoint(3, 0)
    roads.layout()

def test_painful_failure():
    random.seed(1)

    waypoints = [
        [20, 20],
        [20, 80],
        [80, 80],
        [80, 20],
    ]

    roads = RoadNetwork()
    for w in waypoints:
        roads.add_waypoint(*w)

    r_map = roads.layout()