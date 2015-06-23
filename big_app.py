# coding=utf-8

import simpy
from numpy import random

from processes.inventory import Inventory
from processes.fleet import Fleet
from processes.workshop import Workshop

from random_generator import RandomTime

class Simulation(object):

    def __init__(self, replications, total_trucks, design_number,
                 workshop_capacity, n_components, comp_names,
                 life_dist_parameters, repair_dist_parameters,
                 replacement_dist_parameters, start_inventory,
                 simulation_horizon):
        """
        :param replications: the number of replications
        :param total_trucks: the total amount of trucks
        :param design_number: the number of active trucks needed
        :param workshop_capacity: the workshop's capacity
        :param n_components: the number of components,  e.g. 2
        :param comp_names: a list containing the component's names,
        e.g. ["engine", "valve"]
        :param life_dist_parameters: a list describing the lifetime
        distribution of each component. Each element has the form [
        "distribution_name", parameters]. E.g.
        [["exponential", [10]], ["uniform", [0,1]]]
        :param repair_dist_parameters: a list describing the repair time
        distributions. Same format as before.
        :param replacement_dist_parameters: a list describing the replacement
        time distributions. Same format as before.
        :param start_inventory: a list containing the initial inventory for
        each component, e.g. [1, 1]
        :param simulation_horizon:
        """
        self.replications = replications
        self.total_trucks = total_trucks
        self.design_number = design_number
        self.workshop_capacity = workshop_capacity
        self.n_components = n_components
        self.comp_names = comp_names
        self.life_dist_parameters = life_dist_parameters
        self.repair_dist_parameters = repair_dist_parameters
        self.replacement_dist_parameters = replacement_dist_parameters
        self.start_inventory = start_inventory
        self.simulation_horizon = simulation_horizon

        # Output variables

        # Total trucks repaired
        self.total_trucks_repaired = []

        # to be used in graph 1
        self.active_proportion = []
        self.off_proportion = []
        self.stand_by_proportion = []

        # to be used in graph 2
        self.q2_proportion = []
        self.q1_proportion = []
        self.in_ws_proportion = []

        # to be used in graph 3
        self.active_2_proportion = []
        self.total_q_proportion = []
        self.in_ws_2_proportion = []
        self.stand_by_2_proportion = []

        # to be used in graph 4
        self.n_active_mean = []
        self.n_off_mean = []
        self.n_stand_by_mean = []

        # to be used in graph 5
        self.n_q2_mean = []
        self.n_q1_mean = []
        self.n_in_ws_mean = []

        # to be used in graph 6
        self.time = []
        self.active_time = []
        self.off_time = []
        self.stand_by_time = []

        # to be used in graph 7
        self.q2_time = []

        # to be used in graph 8
        self.q1_time = []

        # to be used in graph 9
        self.ws_time = []

        # to be used in graph 14
        self.inventory_time = {}

        # to be used in graph 10
        self.ws_occupation = [[]]*self.workshop_capacity

    def run_simulation(self):

        # set the monitoring time step
        m_step = 1

        # create the output file
        f = open('outputs/data.csv', 'w')
        f.write('Tiempo activo,Tiempo en taller,Tiempo en stand-by,'
                'Tiempo en cola 1,Tiempo en cola 2,Tiempo en taller,Vehiculos '
                'reparados\n')
        f.close()

        for rep in range(self.replications):
            random.seed(rep)
            # create a list containing all component objects
            c_list = []

            for i in range(self.n_components):
                c_list.append([RandomTime(self.life_dist_parameters[i][0],
                                          self.life_dist_parameters[i][1]),
                               RandomTime(self.repair_dist_parameters[i][0],
                                          self.repair_dist_parameters[i][1]),
                               RandomTime(self.replacement_dist_parameters[i][0],
                                          self.replacement_dist_parameters[i][1])])

            # define the initial inventory as a dictionary
            start_inventory = {}
            for i in range(self.n_components):
                start_inventory[self.comp_names[i]] = self.start_inventory[i]

            # create simpy environment
            env = simpy.Environment()
            # create a new inventory
            inv = Inventory(env, start_inventory, m_step)
            # create a new fleet
            fleet = Fleet(1, c_list, self.comp_names, self.total_trucks,
                          self.design_number, env, inv, m_step)
            # create workshops
            for i in range(self.workshop_capacity):
                w = Workshop(env, m_step)

            # run simulation
            env.run(until=self.simulation_horizon)
            print('Simulation finished at %d' % env.now)

            # Get outputs
            out = fleet.get_mean_times()
            mean_times = out[0]
            mean_off_times = out[1]

            out = mean_times + mean_off_times
            out_v = []
            for i in range(len(out)):
                out_v.append(float(out[i])/env.now)

            # save simulation results

            # graphs 1 and 2
            self.active_proportion.append(out_v[0])
            self.off_proportion.append(out_v[1])
            self.stand_by_proportion.append(out_v[2])
            self.q1_proportion.append(out_v[3])
            self.q2_proportion.append(out_v[4])
            self.in_ws_proportion.append(out_v[5])
            self.total_trucks_repaired.append(Workshop.Ndone)

            # graph 3

            sum_t = out[0] + out[3] + out[4] + out[5] + out[2]

            self.active_2_proportion.append(float(out[0])/sum_t)
            self.total_q_proportion.append(float(out[0] + out[4])/sum_t)
            self.in_ws_2_proportion.append(float(out[5])/sum_t)
            self.stand_by_2_proportion.append(float(out[2])/sum_t)

            out = fleet.get_mean_trucks()
            mean_1 = out[0]
            mean_2 = out[1]

            # graphs 4 and 5
            self.n_active_mean.append(mean_1[0])
            self.n_off_mean.append(mean_1[1])
            self.n_stand_by_mean.append(mean_1[2])
            self.n_q1_mean.append(mean_2[0])
            self.n_q2_mean.append(mean_2[1])
            self.n_in_ws_mean.append(mean_2[2])

            # save time evolution output variables
            if rep == 0:
                self.time = fleet.time

                # graph 6
                out = fleet.trucks_count
                self.active_time = out[0]
                self.off_time = out[1]
                self.stand_by_time = out[2]

                out = fleet.queue_count
                # graph 7
                self.q2_time = out[1]
                # graph 8
                self.q1_time = out[0]
                # graph 9
                self.ws_time = fleet.workshop_occupation[0]

                # graph 14
                self.inventory_time = inv.inventory_disp

            # graph 10
            for idx,ws in enumerate(Workshop.All):
                self.ws_occupation[idx].append(ws.get_occupation())

            # print results
            print('I: Active time proportion = %f' % out_v[0])
            print('I: Off time proportion = %f' % out_v[1])
            print('I: Stand-by time proportion = %f' % out_v[2])
            print('I: Queue 1 time proportion = %f' % out_v[3])
            print('I: Queue 2 time proportion = %f' % out_v[4])
            print('I: Workshop time proportion = %f' % out_v[5])
            print('I: Repaired trucks = %f' % Workshop.Ndone)

            # Restart environment variables
            env.event = None
            env.all_of = None
            env._active_proc = None
            env._queue = []
            env.any_of = None
            env._eid = None
            Workshop.Busy = []
            Workshop.Idle = []
            Workshop.Queue_1 = []
            Workshop.Queue_2 = []
            Workshop.next_id = 1
            Workshop.Ndone = 0
            env = None

    def print_pie_file(self):
        file_pie = open('outputs/pie.csv', 'w')

        # write first line
        p = []
        line = ""
        p.append(get_mean(self.active_proportion))
        p.append(get_mean(self.off_proportion))
        p.append(get_mean(self.stand_by_proportion))
        for i in range(len(p)):
            line += "{0:.2f}".format(p[i])
            if i < (len(p) - 1):
                line += ","
            else:
                line += "\n"
        file_pie.write(line)

        # write second line
        p = []
        line = ""
        p.append(get_mean(self.q2_proportion))
        p.append(get_mean(self.q1_proportion))
        p.append(get_mean(self.in_ws_proportion))
        for i in range(len(p)):
            line += "{0:.2f}".format(p[i])
            if i < (len(p) - 1):
                line += ","
            else:
                line += "\n"
        file_pie.write(line)

        # write third line
        p = []
        line = ""
        p.append(get_mean(self.active_2_proportion))
        p.append(get_mean(self.total_q_proportion))
        p.append(get_mean(self.in_ws_2_proportion))
        p.append(get_mean(self.stand_by_2_proportion))
        for i in range(len(p)):
            line += "{0:.2f}".format(p[i])
            if i < (len(p) - 1):
                line += ","
            else:
                line += "\n"
        file_pie.write(line)

        # write fourth line
        p = []
        line = ""
        p.append(get_mean(self.n_active_mean))
        p.append(get_mean(self.n_off_mean))
        p.append(get_mean(self.n_stand_by_mean))
        for i in range(len(p)):
            line += "{0:.2f}".format(p[i])
            if i < (len(p) - 1):
                line += ","
            else:
                line += "\n"
        file_pie.write(line)

        # write fifth line
        p = []
        line = ""
        p.append(get_mean(self.n_q2_mean))
        p.append(get_mean(self.n_q1_mean))
        p.append(get_mean(self.n_in_ws_mean))
        for i in range(len(p)):
            line += "{0:.2f}".format(p[i])
            if i < (len(p) - 1):
                line += ","
            else:
                line += "\n"
        file_pie.write(line)

        file_pie.close()

    def print_time_evolution_files(self):

        l_6 = ""
        l_7 = ""
        l_8 = ""
        l_9 = ""
        l_14 = ""

        for t in range(len(self.time)):
            # write first column
            l_6 += "{0:.1f}".format(self.time[t]) + ","
            l_7 += "{0:.1f}".format(self.time[t]) + ","
            l_8 += "{0:.1f}".format(self.time[t]) + ","
            l_9 += "{0:.1f}".format(self.time[t]) + ","
            l_14 += "{0:.1f}".format(self.time[t]) + ","

            l_6 += str(self.active_time[t]) + "," + str(self.off_time[t]) + \
                   "," + str(self.stand_by_time[t]) + "\n"
            l_7 += str(self.q2_time[t]) + "\n"
            l_8 += str(self.q1_time[t]) + "\n"
            l_9 += str(self.ws_time[t]) + "\n"
            for v in self.inventory_time.values():
                l_14 += "{0:.1f}".format(v[t]) + ","
            l_14 = l_14[:-1]+ "\n"

        f_6 = open("outputs/time_evolution_1.csv", "w")
        f_7 = open("outputs/time_evolution_2.csv", "w")
        f_8 = open("outputs/time_evolution_3.csv", "w")
        f_9 = open("outputs/time_evolution_4.csv", "w")
        f_14 = open("outputs/time_evolution_5.csv", "w")

        f_6.write(l_6)
        f_7.write(l_7)
        f_8.write(l_8)
        f_9.write(l_9)
        f_14.write(l_14)

        f_6.close()
        f_7.close()
        f_8.close()
        f_9.close()
        f_14.close()

    def print_bars_file(self):
        pass


def print_output_to_file(output, headers, file_name):
    f = open(file_name, 'w')
    columns = len(output)
    length = len(output[0])

    line = ""
    for i in range(columns):
        line += headers[i]
        if i < columns-1:
            line += ","
        else:
            line += "\n"

    for row in range(length):
        for col in range(columns):
            line += str(output[col][row])
            if col < columns-1:
                line += ","
            elif row < length-1:
                line += "\n"

    f.write(line)
    f.close()

def get_mean(array):
    if len(array) == 0:
        return 0
    else:
        return float(sum(array))/len(array)


l1 = [["exponential",[10]], ["exponential", [10]]]
s = Simulation(30,3,2,2,2,["c1", "c2"],l1,l1,l1,[1, 1], 365)
s.run_simulation()
s.print_pie_file()
s.print_time_evolution_files()