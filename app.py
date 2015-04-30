"""The app runs from here."""

import simpy
import numpy

from processes.truck import Truck
from processes.workshop import Workshop
from processes.inventory import Inventory
from plotter.console_printer import ConsolePrinter as printer


# Constants
RANDOM_SEED = 42

TRUCKS_AMOUNT = 20 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 15 # Required number of trucks in use at the same time

COMPONENTS = 5 # Number of components
INITIAL_STOCK = 20 # Number of initial stock per component in the inventory

WORKSHOP_CAPACITY = 50 # Amount of parking spot at the workshop

SIM_TIME = 20 # Simulation horizon

def main():
    """Main function to be runned."""

    env = simpy.Environment()

if __name__ == "__main__":
    main()