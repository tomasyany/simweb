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


            
            
