"""The app runs from here."""

import simpy
from processes.workshop import Workshop
from random_generator import RandomTime
from processes.fleet import Fleet
from processes.inventory import Inventory
# from plotter.console_printer import ConsolePrinter as printer


# Constants
RANDOM_SEED = 42

TRUCKS_AMOUNT = 2 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 2 # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = 2

COMPONENTS = 5 # Number of components
LIFETIME_MEAN = 24*365*4
REPAIRTIME_MEAN = 24
REPLACEMENTTIME_MEAN = 24*30
start_inventory = {1 : 2, 2 : 2 ,3 : 2, 4 : 2}

SIMULATION_HORIZON = 24*365*20

def main():
    """Main function to be runned."""

#<<<<<<< HEAD
 #   printer.welcome() # Welcome message

    env = simpy.Environment()
    # lifetime, repair time and inventory replacement time distributions for each distribution
    c = []
    for i in range(COMPONENTS):
        c.append([RandomTime('exponential',LIFETIME_MEAN), 
            RandomTime('exponential',REPAIRTIME_MEAN), 
            RandomTime('exponential',REPLACEMENTTIME_MEAN)])

    inv = Inventory(env,start_inventory)
    fleet = Fleet(1,c,[1,2,3,3,4],TRUCKS_AMOUNT,TRUCKS_USE,env,inv)
    for i in range(WORKSHOP_CAPACITY):
        w = Workshop(env)

    env.run(until=SIMULATION_HORIZON)
    print('Simulation finished at %d' % env.now)
    mean_times = fleet.get_mean_times()
    output = [float(mean_times[0])/env.now, float(mean_times[1])/env.now,
              float(mean_times[
        2])/env.now]
    print('Active time proportion = %f' % output[0])
    print('Off time proportion = %f' % output[1])
    print('Stand-by time proportion = %f' % output[2])


if __name__ == "__main__":
    main()
