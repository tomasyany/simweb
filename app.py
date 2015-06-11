"""The app runs from here."""

import sys
import simpy
from processes.workshop import Workshop
from random_generator import RandomTime
from processes.fleet import Fleet
from processes.inventory import Inventory

# from plotter.console_printer import ConsolePrinter as printer


# Constants
TRUCKS_AMOUNT = sys.argv[0] # Total number of trucks (in use, at workshop or
# standing-by)
TRUCKS_USE = sys.argv[1] # Required number of trucks in use at the same time

WORKSHOP_CAPACITY = sys.argv[2]

COMPONENTS = sys.argv[3] # Number of components
C_NAMES = sys.argv[4]

life_dist = sys.argv[5]
repair_dist = sys.argv[6]
replacement_dist = sys.argv[7]

C_LIST =[]
for i in range(COMPONENTS):
    C_LIST.append([RandomTime(life_dist[0],life_dist[1]), RandomTime(
        repair_dist[0],repair_dist[1]), RandomTime(replacement_dist[0],
                    replacement_dist[1])])

start_inventory = {}
for i in range(COMPONENTS):
    start_inventory[C_NAMES[i]] = sys.argv[8][i]


SIMULATION_HORIZON = sys.argv[9]


def run():
    env = simpy.Environment()
    inv = Inventory(env,start_inventory)
    fleet = Fleet(1,C_LIST,C_NAMES ,TRUCKS_AMOUNT,TRUCKS_USE,env,inv)
    for i in range(WORKSHOP_CAPACITY):
        w = Workshop(env)

    env.run(until=SIMULATION_HORIZON)
    print('Simulation finished at %d' % env.now)
    mean_times = fleet.get_mean_times()
    out_v = [float(mean_times[0])/env.now, float(mean_times[1])/env.now,
             float(mean_times[2])/env.now]
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
    """Main function to be runned."""

    #<<<<<<< HEAD
    #   printer.welcome() # Welcome message

    r = run()

    my_file = open('data.csv', 'a')
    my_line = ""
    for i in range(0, len(r)):
        my_line += str(r[i])
        if i<len(r)-1:
            my_line += ","
    my_line += "\n"
    my_file.write(my_line)
    my_file.close()

if __name__ == "__main__":
    main()
