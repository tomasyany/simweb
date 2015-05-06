"""The fleet class. This represents a fleet of trucks."""

from processes.truck import Truck
from processes.component import Component
import simpy

class Fleet(object):

    def __init__(self, fleet_id,component_distributions,type_list,n_trucks,
                 design_number,
                 env,inventory):
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
        self.inventory = inventory

        # Create n_trucks and add them to active_trucks or to stand_by_trucks
        for i in range(n_trucks):
            # we create a new truck
            truck = Truck(env, 1000*self.fleet_id+truck_id, None, self,
                          self.inventory)
            truck_id += 1
            # for each truck we create a list containing its components
            components = []
            # component_distributions is a list in which each element is a
            # list of three RandomTime objects
            for idx, c in enumerate(component_distributions):
                components.append(Component(env,truck,c[0],c[1],c[2],
                                            type_list[idx]))
            truck.components = components

            # check whether the created truck is activated or not
            if i < design_number:
                truck.activate_event.succeed()
                self.active_trucks.append(truck)
            else:
                self.stand_by_trucks.append(truck)

    def get_mean_times(self):
        active_time = 0
        off_time = 0
        stand_by_time = 0
        for truck in self.active_trucks + self.off_trucks + \
                self.stand_by_trucks:
            active_time += truck.get_output_times()[0]
            off_time += truck.get_output_times()[1]
            stand_by_time += truck.get_output_times()[2]
        mean_active = float(active_time)/self.n_trucks
        mean_off = float(off_time)/self.n_trucks
        mean_sb = float(stand_by_time)/self.n_trucks
        return [mean_active, mean_off, mean_sb]