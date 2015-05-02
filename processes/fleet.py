"""The fleet class. This represents a fleet of trucks."""

from processes.truck import Truck
from processes.component import Component
import simpy

class Fleet(object):

    def __init__(self, fleet_id,component_distributions,n_trucks,design_number,
                 env):
        """The contructor of the Fleet class."""

        self.fleet_id = fleet_id
        # n_trucks is the total amount of trucks in this fleet
        self.n_trucks = n_trucks
        self.env = env    # the simpy environment
        # design_number is the number of trucks that have to be active
        self.design_number = design_number
        truck_id = 1    # this variable is used for indexing the trucks of
        # this fleet
        self.active_trucks = []    # list containing the active trucks
        self.stand_by_trucks = []    # list containg the trucks in stand-by
        self.off_trucks = []    # list contaning the trucks in the repair
        # process

        # Create n_trucks and add them to active_trucks or to stand_by_trucks
        for i in range(n_trucks):
            # we create a new truck
            truck = Truck(env, 1000*self.fleet_id+truck_id, None, self)
            truck_id += 1
            # for each truck we create a list containing its components
            components = []
            # component_distributions is a list in which each element is a
            # list of three RandomTime objects
            for c in component_distributions:
                components.append(Component(env,truck,c[0],c[1],c[2]))
            truck.components = components

            # check whether the created truck is activated or not
            if i < design_number:
                truck.activate_event.succeed()
                self.active_trucks.append(truck)
            else:
                self.stand_by_trucks.append(truck)
