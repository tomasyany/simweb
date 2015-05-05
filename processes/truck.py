"""Process that represent a truck entity"""

from processes.workshop import Workshop
class Truck(object):
    """ A truck is represented as a process. It has components that
    may fail and thus cause the truck to need reparation.
    Trucks wait for an empty workshop and the for the reparation process to be
    completed.
    Repaired trucks can go either active (working) or stand-by """

    repair_time = 0   # time of last reparation = 0 by default

    def __init__(self,env,t_id,components,fleet,inventory):
        """" Constructor for the Truck process"""
        # components is a list containing all the components of this truck
        self.components = components
        self.env = env    # simpy environment
        self.id = t_id    # truck id
        self.fleet = fleet     # The fleet this truck belongs to
        self.inventory = inventory

        # Tell simpy to add this truck's run() process
        self.action = env.process(self.run())

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

        # The following are variables that may be used for calculating output
        #  variables
        # total working time
        self.working_time = 0
        # the total amount of time this truck is neither working nor stand-by
        self.off_time = 0
        # the total amount of time this truck is in stand-by
        self.standby_time = 0


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

            # Update the total time spent in stand-by
            self.standby_time += self.env.now-self.repair_time
            start_time = self.env.now

            print('Truck # %d started working at %d' %(self.id, self.env.now))

            # Step 2: wait until the fail_event is triggered by one the
            # truck's components
            yield self.fail_event
            self.fail_event = self.env.event()

            # Update the total working time
            self.working_time +=self.env.now-start_time

            self.failure()    # call the failure method
            failure_time = self.env.now # update the last failure time

            #Step 3: Remove the truck from the active list and send it to the
            #  Workshop's queue
            self.fleet.active_trucks.remove(self)
            self.fleet.off_trucks.append(self)
            Workshop.Queue.append(self)
            # If there are any idle workshop we tell one of them that it's
            # been required for a repair process
            if Workshop.Idle != []:
                Workshop.Idle[0].required.succeed()

            #Step 4: Wait until the repair_event has been triggered
            yield self.repair_event
            self.repair_event = self.env.event()
            # update the total off time
            self.off_time += self.env.now - failure_time
            self.repair_time = self.env.now

    def failure(self):
        # The failure method. It checks whether there are trucks in stand-by
        # to replace the failing truck
        print('Truck # %d stopped working at %d' % (self.id, self.env.now))
        self.inventory.request_component(self)
        if self.fleet.stand_by_trucks != []:
            truck = self.fleet.stand_by_trucks.pop(0)
            # Trigger the activate_event of new truck
            truck.activate_event.succeed()
            self.fleet.active_trucks.append(truck)
