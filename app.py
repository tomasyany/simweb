"""The app runs from here."""

import simpy
from processes.workshop import Workshop
from random_generator import RandomTime
from processes.fleet import Fleet
from processes.inventory import Inventory
# from plotter.console_printer import ConsolePrinter as printer


# Constants
RANDOM_SEED = 42

TRUCKS_AMOUNT = 20 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 15 # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = 1

COMPONENTS = 5 # Number of components
LIFETIME_MEAN = 24*365*4
REPAIRTIME_MEAN = 24*10
REPLACEMENTTIME_MEAN = 24*30

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

    start_inventory = {1 : 1, 2 : 1 ,3 : 1, 4 : 0}
    inv = Inventory(env,start_inventory)
    fleet = Fleet(1,c,[1,2,3,3,4],TRUCKS_AMOUNT,TRUCKS_USE,env,inv)
    for i in range(WORKSHOP_CAPACITY):
        w = Workshop(env)

    env.run(until=SIMULATION_HORIZON)

if __name__ == "__main__":
    main()
