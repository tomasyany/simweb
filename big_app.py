import sys
import simpy
import matplotlib.pyplot as plt

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

    def run_simulation(self):
        sys.argv = [self.total_trucks, self.design_number,
                    self.workshop_capacity, self.n_components,
                    self.comp_names, self.life_dist_parameters,
                    self.repair_dist_parameters,
                    self.replacement_dist_parameters,self.start_inventory,
                    self.simulation_horizon]

        f = open('outputs/data.csv', 'w')
        f.write('Tiempo activo,Tiempo en taller,Tiempo en stand-by,'
        'Vehiculos reparados\n')
        f.close()

        for i in range(self.replications):
            exec(open('app.py').read())

        print("end")

    def gen_plots(self):
        output = [[], [], []]
        with open('outputs/data.csv') as f:
            for idx,line in enumerate(f):
                if idx == 0:
                    labels = line.split(',')[:3]
                else:
                    aux = line.split(',')[:3]
                    for i in range(3):
                        output[i].append(float(aux[i]))

        m1 = self.get_means(output[0])
        m2 = self.get_means(output[1])
        m3 = self.get_means(output[2])

        self.pie_plot1(labels,[m1, m2, m3])

    def get_means(self,array):
        if len(array)==0:
            return 0
        else:
            r = 0
            for i in range(len(array)):
                r += array[i]
            r /= len(array)
            return r

    def pie_plot1(self, labels, sizes):
        explode = (0.05, 0.05, 0.05)
        colors = ['yellowgreen', 'lightskyblue', 'lightcoral']
        plt.pie(sizes, explode = explode, labels = labels, autopct =
        '%1.1f%%', colors=colors, shadow=True, startangle=90)
        plt.axis('equal')
        plt.savefig('fig1.pdf')

l1 = [["exponential",[10]], ["exponential", [10]]]
s = Simulation(30,3,2,2,2,["c1", "c2"],l1,l1,l1,[1, 1], 365)
s.run_simulation()