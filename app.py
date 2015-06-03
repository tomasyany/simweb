"""The app runs from here."""

import simpy
from processes.workshop import Workshop
from random_generator import RandomTime
from processes.fleet import Fleet
from processes.inventory import Inventory
from processes.truck import Truck
from processes.component import Component
# from plotter.console_printer import ConsolePrinter as printer


# Constants
RANDOM_SEED = 42

REPLICATIONS = 1

TRUCKS_AMOUNT = 20 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 15 # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = 4

COMPONENTS = 3 # Number of components
LIFETIME_MEAN = [24*1, 24*7, 24 *3]
REPAIRTIME_MEAN = [[5,10], [12, 24], [12,20]]
REPLACEMENTTIME_MEAN = [[2,24], [3,24], [3,12]]
start_inventory = {1 : 2, 2 : 1, 3 : 1 }
t_list = [1, 2, 3]

SIMULATION_HORIZON = 24*365


def run():
    env = simpy.Environment()
    # lifetime, repair time and inventory replacement time distributions for each distribution
    c = []
    for i in range(COMPONENTS):
        c.append([RandomTime('exponential',LIFETIME_MEAN[i]),
            RandomTime('uniform',REPAIRTIME_MEAN[i]),
            RandomTime('gamma',REPLACEMENTTIME_MEAN[i])])

    inv = Inventory(env,start_inventory)
    fleet = Fleet(1,c,t_list,TRUCKS_AMOUNT,TRUCKS_USE,env,inv)
    for i in range(WORKSHOP_CAPACITY):
        w = Workshop(env)

    env.run(until=SIMULATION_HORIZON)
    print('Simulation finished at %d' % env.now)
    mean_times = fleet.get_mean_times()
    out_v = [float(mean_times[0])/env.now, float(mean_times[1])/env.now,
              float(mean_times[
        2])/env.now]
    out_v.append(Workshop.Ndone)

    print('I: Active time proportion = %f' % out_v[0])
    print('I: Off time proportion = %f' % out_v[1])
    print('I: Stand-by time proportion = %f' % out_v[2])
    print('I: Repaired trucks = %f' % out_v[3])


    # Restart environment variables
    env.event = None
    env.all_of = None
    env._active_proc = None
    env._queue = None
    env.any_of = None
    env._eid = None
    Workshop.Busy = []
    Workshop.Idle = []
    Workshop.Queue_1 = []
    Workshop.Queue_2 = []
    Workshop.next_id = 1
    Workshop.Ndone = 0
    env = None


    return out_v

def main():
    """Main function to be  runned."""

    #<<<<<<< HEAD
    #   printer.welcome() # Welcome message

    r = run()

    my_file = open('output.txt', 'a')
    my_line = ""
    for i in range(0, len(r)):
           my_line += str(r[i])+"\t"
    my_line += "\n"
    my_file.write(my_line)
    my_file.close()

if __name__ == "__main__":
    main()
