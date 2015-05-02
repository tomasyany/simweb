"""Process that represents the truck entity.
(We use processes because of a simpy convention.)"""

from numpy.random import normal
from simpy import Interrupt

class Truck(object):
    """A truck is represented as a process. 

    It has a time to fail, a time to next maintenance.
    It can be in four different states: in use, stand-by, at workshop,
    in the queue for the workshop.
    """

    def __init__ (self, env, truck_id):
        """Constructor for the Truck process."""
        self.env = env

        self.truck_id = truck_id

        self.has_failure = False
        self.has_maint: = False

        self.in_use = True
        self.in_standby = False
        self.in_queue = False
        self.in_workshop = False

        self.components = components # list containing all the components of this truck
        self.fleet = fleet
        self.action = env.process(self.run())
        self.fail_event = env.event() # the event when this truck fails
        self.activate_event = env.event() # the event when this truck becomes active
        self.repair_event = env.event() # the event when this truck has been repaired
        self.working_time = 0 # total working time
        self.off_time = 0 # the total amount of time this truck is neither working nor stand-by
        self.standby_time = 0 # the total amount of time this truck is in stand-by
        self.comp_repair_time = 0 # this is the time required to be repaired (it may change each time this truck fails)
        self.comp_inventory_time = 0 # failed component's lead time

        print ("Truck number "+str(self.truck_id)+" has entered simulation.")

    def time_to_failure():
        """Returns the time for the next failure to happen."""
        return normal(0,1) #TODO

    def time_to_maintenance():
        """Returns the time for the next maintenance to happen."""
        return normal(0,1) #TODO

    def stops_truck():
        """Calls for a failure or a maintenance."""
        while True:
            if self.in_use == True:
                # Only stops the truck if it is actually working
                self.process.interrupt()


    def in_use(self):
        """The truck is in use as long as one of its components doesn't fail
        or and scheduled maintenance has to be done."""

        while True:
            try:
                start = self.env.now

            except Interrupt:
                self.has_failure = True

    def run(self):
    """ The run process. The truck waits to be activated. Then it works until one of its components
    triggers the fail event and the truck goes off. After this, the truck goes to the Workshop queue 
    and waits until the repair event is triggered. """

        while True:
            yield self.activate_event
            self.activate_event = self.env.event()
            self.standby_time += self.env.now-self.repair_time
            start_time = self.env.now

            print('Truck # %d started working at %d' %(self.truck_id, self.env.now))

            yield self.fail_event

            self.fail_event = self.env.event()
            self.working_time +=self.env.now-start_time
            self.failure()
            failure_time = self.env.now
            self.fleet.active_trucks.remove(self)
            self.fleet.off_trucks.append(self)
            Workshop.Queue.append(self)

            if Workshop.Idle != []:
                Workshop.Idle[0].required.succeed()

            yield self.repair_event

            self.repair_event = self.env.event()
            self.off_time += self.env.now - failure_time
            self.repair_time = self.env.now

    def failure(self):
        print('Truck # %d stopped working at %d' % (self.truck_id, self.env.now))

        if self.fleet.stand_by_trucks != []:
            truck = self.fleet.stand_by_trucks.pop(0)
            truck.activate_event.succeed()
            self.fleet.active_trucks.append(truck)
