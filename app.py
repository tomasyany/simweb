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

TRUCKS_AMOUNT = 2 # Total number of trucks (in use, at workshop or standing-by)
TRUCKS_USE = 2 # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = 2

COMPONENTS = 2 # Number of components
LIFETIME_MEAN = 24*1
REPAIRTIME_MEAN = 24*0.5
REPLACEMENTTIME_MEAN = 24*0.5
start_inventory = {1 : 1, 2 : 1 }
t_list = [1,2]

SIMULATION_HORIZON = 24*365*1


def run():
    env = simpy.Environment()
    # lifetime, repair time and inventory replacement time distributions for each distribution
    c = []
    for i in range(COMPONENTS):
        c.append([RandomTime('exponential',LIFETIME_MEAN),
            RandomTime('exponential',REPAIRTIME_MEAN),
            RandomTime('exponential',REPLACEMENTTIME_MEAN)])

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

    print('I: Active time proportion = %f' % out_v[0])
    print('I: Off time proportion = %f' % out_v[1])
    print('I: Stand-by time proportion = %f' % out_v[2])

    return out_v

def main():
    """Main function to be runned."""

    #<<<<<<< HEAD
    #   printer.welcome() # Welcome message

    output_active = []
    output_off = []
    output_standby = []
    for i in range(REPLICATIONS):
        r = run()
        output_active.append(r[0])
        output_off.append(r[1])
        output_standby.append(r[2])

    print(output_active)
    print(output_off)
    print(output_standby)
    print Workshop.Ndone


if __name__ == "__main__":
    main()
