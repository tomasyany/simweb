"""This class describes the workshop as a process"""


class Workshop(object):
    """Each Workshop represents a place where a truck can be repaired.
    Workshops remain idle until they are required by incoming trucks,
    then they stay busy until no more trucks are waiting to be repaired.
        """

    next_id = 1    # for indexing different workshops
    Idle = []    # idle workshops
    Busy = []    # busy workshops
    Queue_1 = []    # trucks with component waiting to be repaired
    Queue_2 = []    # trucks without component waiting to be repaired
    Ndone = 0    # total amount of repaired trucks

    def __init__(self, env, mon_step):
        """ Constructor for the Workshop process"""
        self.env = env    # the simpy environment
        self.monitor_step = mon_step # monitoring time step

        # Set a different id for each workshop
        self.id = Workshop.next_id
        Workshop.next_id += 1

        # Tell simpy to add this workshop's run() process
        self.action = env.process(self.run())

        Workshop.Idle.append(self)  # all workshops start as idle

        # The required event is triggered when this workshop is idle and
        # there is an incoming repair request
        self.required = env.event()

    def run(self):
        """ The run process.
        1) Wait until a repair job is required
        2) Work while there are trucks in the queue
        3) Turn idle again
        """
        while True:
            # Step 1: wait until the required event has been triggered
            yield self.required
            self.required = self.env.event()
            print('Workshop # %d has been required at %d' %(self.id,
                                                            self.env.now))
            # Remove this workshop from the idle list
            Workshop.Idle.remove(self)
            Workshop.Busy.append(self)

            # Step 2: Repair process
            while Workshop.Queue_1 != [] or Workshop.Queue_2 != []:
                # get the first truck in the queue
                if Workshop.Queue_1 != []:
                    truck = Workshop.Queue_1.pop(0)
                    truck.l_q1_time = self.env.now
                    truck.t_queue1_time += self.env.now - truck.l_q2_time
                else:
                    truck = Workshop.Queue_2.pop(0)
                    truck.l_q1_time = self.env.now
                    truck.l_q2_time = self.env.now
                    truck.t_queue2_time += self.env.now - truck.failure_time

                yield self.env.process(self.repair_truck(truck))

            # Step 3: Once all repair jobs have been done the workshop turns
            # idle again
            Workshop.Busy.remove(self)
            Workshop.Idle.append(self)

    def repair_truck(self, truck):
        # wait until the replacement component has arrived
        yield truck.got_component
        truck.got_component = self.env.event()
        # wait for the repair job to be done
        print('Workshop # %d has begun repair process on truck # %d at %d' %(
            self.id, truck.id, self.env.now))
        yield self.env.timeout(truck.comp_repair_time)
        print('Truck # %d was repaired by workshop # %d at %d' % (
            truck.id, self.id, self.env.now))
        # Trigger the repair event: it tells the truck it's been
        # repaired
        truck.repair_event.succeed()
        # increase the amounts of done jobs
        Workshop.Ndone += 1
        # remove the repaired truck from the off list
        truck.fleet.off_trucks.remove(truck)
        # check whether the repaired has to turn active or into stand-by
        if len(truck.fleet.active_trucks) < truck.fleet.design_number:
            # if there are not enough active trucks then the repaired
            #  truck is activated immediately
            truck.activate_event.succeed()    # trigger the
            # activate_event
            truck.fleet.active_trucks.append(truck)
        else:
            truck.fleet.stand_by_trucks.append(truck)