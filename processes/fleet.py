"""The fleet class. This represents a fleet of trucks."""

from truck import Truck
from component import Component
import simpy

class Fleet(object):

    def __init__(self, id,component_distributions,n_trucks,design_number,env):
	"""The contructor of the Fleet class."""
        self.fleet_id = id
        self.n_trucks = n_trucks
        self.env = env
        self.design_number = design_number
        truck_id = 1
        self.active_trucks = []
        self.stand_by_trucks = []
        self.off_trucks = []

        for i in range(n_trucks):
            components = []
            truck = Truck(env, 1000*self.fleet_id+truck_id, None, self)
            truck_id += 1

            for c in component_distributions:
                components.append(Component(env,truck,c[0],c[1],c[2]))
            truck.components = components

            if i < design_number:
                truck.activate_event.succeed()
                self.active_trucks.append(truck)
            else:
                self.stand_by_trucks.append(truck)
