"""This class describes the workshop as a resource."""

from simpy import Resource

class Workshop (object):
    """A workshop has a limited number of parking spots (WORKSHOP_CAPACITY) to 
    repair/maitain trucks in parallel.

    Trucks have to request one of the spots. When they got one, the repair/
    maintain process can start and they'll will wait an amount of time for it 
    to finish.
    """

    def __init__(self, env, workshop_capacity):
        # TODO = add repair/maintain time
        self.env = env
        self.spot = Resource(env, workshop_capacity)

    def repair (self, truck):
        """The repair process. It takes a truck process and repairs it."""

        repair_time = #TODO
        yield self.env.timeout(repair_time)


    def repair (self, truck):
        """The maintain process. It takes a truck process and performs 
        a maintenance."""
        
        maint_time = #TODO
        yield self.env.timeout(maint_time)
