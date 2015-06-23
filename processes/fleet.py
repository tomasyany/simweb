"""The fleet class. This represents a fleet of trucks."""

from processes.truck import Truck
from processes.component import Component
from processes.workshop import Workshop
import simpy

class Fleet(object):

    def __init__(self, fleet_id,component_distributions,type_list,n_trucks,
                 design_number, env, inventory, monitor_step):
        """ The constructor of the Fleet class."""

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
        # the monitoring time step
        self.monitor_step = monitor_step

        # trucks count stores the amount of active, off and stand-by trucks
        # at every monitoring time step
        self.trucks_count = [[], [], []]

        # queue count stores the amount of trucks waiting in queue 1 and 2 at
        #  every monitoring time step
        self.queue_count = [[], []]

        # workshop occupation stores the amount of busy and idle workshops at
        #  every monitoring time step
        self.workshop_occupation = [[], []]

        self.monitor_process = self.env.process(self.monitor_fleet())

        # Create n_trucks and add them to active_trucks or to stand_by_trucks
        for i in range(n_trucks):
            # we create a new truck
            truck = Truck(env, 1000*self.fleet_id+truck_id, None, self,
                          self.inventory, self.monitor_step)
            truck_id += 1
            # for each truck we create a list containing its components
            components = []
            # component_distributions is a list in which each element is a
            # list of three RandomTime objects
            for idx, c in enumerate(component_distributions):
                components.append(Component(env, truck, c[0], c[1], c[2],
                                            type_list[idx]))
            truck.components = components

            # check whether the created truck is activated or not
            if i < design_number:
                truck.activate_event.succeed()
                self.active_trucks.append(truck)
            else:
                self.stand_by_trucks.append(truck)

    def monitor_fleet(self):
        while True:
            self.trucks_count[0].append(len(self.active_trucks))
            self.trucks_count[1].append(len(self.off_trucks))
            self.trucks_count[2].append(len(self.stand_by_trucks))

            self.queue_count[0].append(len(Workshop.Queue_1))
            self.queue_count[1].append(len(Workshop.Queue_2))

            self.workshop_occupation[0].append(len(Workshop.Busy))
            self.workshop_occupation[1].append(len(Workshop.Idle))

            yield self.env.timeout(self.monitor_step)

    def get_mean_times(self):
        active_time = 0
        off_time = 0
        stand_by_time = 0
        q1_time = 0
        q2_time = 0
        ws_time = 0

        for truck in self.active_trucks + self.off_trucks + \
                self.stand_by_trucks:
            out = truck.get_output_times()
            t_out_times = out[0]
            t_out_off_times = out[1]

            active_time += t_out_times[0]
            off_time += t_out_times[1]
            stand_by_time += t_out_times[2]

            q1_time += t_out_off_times[0]
            q2_time += t_out_off_times[1]
            ws_time += t_out_off_times[2]

        mean_active = float(active_time)/self.n_trucks
        mean_off = float(off_time)/self.n_trucks
        mean_sb = float(stand_by_time)/self.n_trucks

        mean_q1 = float(q1_time)/self.n_trucks
        mean_q2 = float(q2_time)/self.n_trucks
        mean_ws = float(ws_time)/self.n_trucks

        output1 = [mean_active, mean_off, mean_sb]
        output2 = [mean_q1, mean_q2, mean_ws]

        return [output1, output2]

    def get_mean_trucks(self):
        mean_active = sum(self.trucks_count[0])/float(len(self.trucks_count[0]))
        mean_off = sum(self.trucks_count[1])/float(len(self.trucks_count[1]))
        mean_sb = sum(self.trucks_count[2])/float(len(self.trucks_count[2]))

        mean_q1 = sum(self.queue_count[0])/float(len(self.queue_count[0]))
        mean_q2 = sum(self.queue_count[1])/float(len(self.queue_count[1]))
        mean_ws = sum(self.workshop_occupation[0])/float(len(
            self.workshop_occupation[0]))

        output1 = [mean_active, mean_off, mean_sb]
        output2 = [mean_q1, mean_q2, mean_ws]

        return [output1, output2]
