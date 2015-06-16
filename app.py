"""The app runs from here."""

print(sys.argv)


def main():

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
        C_LIST.append([RandomTime(life_dist[i][0],life_dist[i][1]), RandomTime(
            repair_dist[i][0],repair_dist[i][1]), RandomTime(
            replacement_dist[i][0], replacement_dist[i][1])])

    start_inventory = {}
    for i in range(COMPONENTS):
        start_inventory[C_NAMES[i]] = sys.argv[8][i]

    SIMULATION_HORIZON = sys.argv[9]


    env = simpy.Environment()
    inv = Inventory(env, start_inventory)
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


    r = out_v


if __name__ == "__main__":
    main()
