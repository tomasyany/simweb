"""The app runs from here."""

import simpy
import numpy

from truck import Truck
from workshop import Workshop
from random_generator import RandomTime
from fleet import Fleet


# Constants
RANDOM_SEED = 42

TRUCKS_AMOUNT = 20 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 15 # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = 4

COMPONENTS = 5 # Number of components
LIFETIME_MEAN = 20
REPAIRTIME_MEAN = 5
REPLACEMENTTIME_MEAN = 3

SIMULATION_HORIZON = 1000

def main():
    """Main function to be runned."""

    printer.welcome() # Welcome message

    env = simpy.Environment()
    # lifetime, repair time and inventory replacement time distributions for each distribution
    c = []
    for i in range(COMPONENTS):
        c.append([RandomTime('exponential',LIFETIME_MEAN), 
            RandomTime('exponential',REPAIRTIME_MEAN), 
            RandomTime('exponential',REPLACEMENTTIME_MEAN)])

    fleet = Fleet(1,c,TRUCKS_AMOUNT,TRUCKS_USE,env)
    for i in range(WORKSHOP_CAPACITY):
        w = Workshop(env)

    env.run(until=SIMULATION_HORIZON)

if __name__ == "__main__":
    main()