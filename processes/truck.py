"""Process that represent a truck entity"""

from processes.workshop import Workshop


class Truck(object):
    """ A truck is represented as a process. It has components that
    may fail and thus cause the truck to need reparation.
    Trucks wait for an empty workshop and the for the reparation process to be
    completed.
    Repaired trucks can go either active (working) or stand-by """

    def __init__(self, env, t_id, components, fleet, inventory, mon_step):
        """" Constructor for the Truck process"""
        # components is a list containing all the components of this truck
        self.components = components
        self.env = env    # simpy environment
        self.id = t_id    # truck id
        self.fleet = fleet     # The fleet this truck belongs to
        self.inventory = inventory
        self.monitor_step = mon_step  # monitoring time step

        # Tell simpy to add this truck's run() and check_component() processes
        self.action = env.process(self.run())
        self.check = env.process(self.check_component())

        # The following are events that tell us when the truck has failed,
        # when it has been repaired and when it has been activated (it has
        # become operative).

        # The fail event is triggered when a component fails
        self.fail_event = env.event()
        # The activate event may be triggered at the beginning of the simulation
        # or when a truck passes from stand-by to active
        self.activate_event = env.event()
        # The repair event is triggered when the workshop is done with repair
        #  process
        self.repair_event = env.event()
        # The got component event is triggered when a truck gets the
        # component needed to achieve the repair process
        self.got_component = env.event()

        # The following variables might be used for calculating output
        #  variables
        # total working time
        self.working_time = 0
        # the total amount of time this truck is neither working nor stand-by
        self.off_time = 0
        # the total amount of time this truck is in stand-by
        self.standby_time = 0
        # total amount of time spent in queue 2
        self.t_queue2_time = 0
        # total amount of time spent in queue 1
        self.t_queue1_time = 0
        # total amount of time spent in the workshop
        self.t_workshop_time = 0

        # the last failure time
        self.failure_time = 0
        # the last repair time
        self.repair_time = 0
        # the last activation time
        self.start_time = 0
        # last time truck left queue_2
        self.l_q2_time = 0
        # last time truck left queue_1
        self.l_q1_time = 0

        # the current state = 'active', 'off' or 'stand_by'
        self.state = 'stand_by'

        # this is the time required to be repaired (it may change each time
        # this truck fails)
        self.comp_repair_time = 0
        # failed component's lead time
        self.comp_inventory_time = 0
        self.comp_type = 0

    def run(self):
        """ The run process.
        1) The truck waits to be activated
        2) The truck waits until one of its components has failed
        3) Send this truck to queue of trucks waiting for an empty workshop
        4) Wait until the repair process has concluded
         """
        while True:
            # Step 1: wait until the activate_event has been triggered
            yield self.activate_event
            # We set the activate_event to a new event that hasn't been
            # triggered yet
            self.activate_event = self.env.event()
            self.state = 'active'    # set current state to 'active'

            # Update the total time spent in stand-by
            self.standby_time += self.env.now-self.repair_time
            self.start_time = self.env.now

            print('Truck # %d started working at %f' %(self.id, self.env.now))

            # Step 2: wait until the fail_event is triggered by one the
            # truck's components
            yield self.fail_event
            self.fail_event = self.env.event()
            self.state = 'off'    # set current state to 'off'
            self.failure_time = self.env.now # update the last failure time

            # Update the total working time
            self.working_time +=self.env.now-self.start_time

            self.failure()    # call the failure method

            # Step 3: Remove the truck from the active list and add it to the
            # off list
            self.fleet.active_trucks.remove(self)
            self.fleet.off_trucks.append(self)

            # If there are any idle workshop we tell one of them that it's
            # been required for a repair process
            if Workshop.Idle != []:
                Workshop.Idle[0].required.succeed()

            #Step 4: Wait until the repair_event has been triggered
            yield self.repair_event
            self.repair_event = self.env.event()

            self.state = 'stand_by'    # set current state to 'stand_by'
            # update the total off time
            self.off_time += self.env.now - self.failure_time
            self.repair_time = self.env.now    # update last repair time
            self.t_workshop_time += self.env.now - self.l_q1_time

    def failure(self):
        # The failure method. It checks whether there are trucks in stand-by
        # to replace the failing truck
        print('Truck # %d stopped working at %f' % (self.id, self.env.now))

        # Send the truck to the workshop's queue
        Workshop.Queue_2.append(self)
        print('Truck # %d has entered queue 2 at %f' % (self.id, self.env.now))
        self.inventory.request_component(self)
        if self.fleet.stand_by_trucks != []:
            truck = self.fleet.stand_by_trucks.pop(0)
            # Trigger the activate_event of new truck
            truck.activate_event.succeed()
            self.fleet.active_trucks.append(truck)

    def check_component(self):
        # Check whether the replacement component has been provided in order
        # to take the truck from Queue_2 to Queue_1
        while True:
            yield self.fail_event
            yield self.got_component
            if self in Workshop.Queue_2:
                Workshop.Queue_2.remove(self)
                Workshop.Queue_1.append(self)
                # self.insert_in_order()
                self.l_q2_time = self.env.now
                self.t_queue2_time += self.env.now - self.failure_time
                print('Truck # %d has entered queue 1 at %f' % (self.id,
                      self.env.now))

    def insert_in_order(self):
        for idx, truck in enumerate(Workshop.Queue_1):
            index = -1
            if truck.failure_time > self.failure_time:
                index = idx
                break
            if index == -1:
                Workshop.Queue_1.append(self)
            else:
                Workshop.Queue_1 = Workshop.Queue_1[:index] + [self] + \
                                   Workshop.Queue_1[index:]

    def get_output_times(self):
        # This method returns the total working time, the total off time and
        # the total stand-by time at the end of the simulation

        if self.state == 'active':
            self.working_time += self.env.now - self.start_time
        elif self.state == 'off':
            self.off_time += self.env.now - self.failure_time

            if (self.l_q2_time > self.l_q1_time) & (self.l_q2_time >
                    self.repair_time):
                self.t_queue1_time += self.env.now - self.l_q2_time
            elif (self.l_q1_time > self.l_q2_time) & (self.l_q1_time > \
                    self.repair_time):
                self.t_workshop_time += self.env.now - self.l_q1_time
            else:
                self.t_queue2_time += self.env.now - self.failure_time

        else:
            self.standby_time += self.env.now - self.repair_time

        output_1 = [self.working_time, self.off_time, self.standby_time]
        output_2 = [self.t_queue2_time, self.t_queue1_time, self.t_workshop_time]

        return [output_1, output_2]
