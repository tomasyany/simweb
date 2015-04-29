"""Process that represents the truck entity.
(We use processes because of a simpy convention.)"""

class Truck(object):

    def __init__ (self, env, truck_id, ):
        """Constructor for the Truck process."""

        self.env = env
        self.action = env.process(self.run())
        self.truck_id = truck_id
        print ("Truck number "+self.truck_id+" has entered simulation.")

    def run(self):
        while True:
            pass
            break
