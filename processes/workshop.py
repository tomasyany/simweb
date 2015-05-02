"""This class describes the workshop as a resource."""

from simpy import PriorityResource

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
        self.spot = PriorityResource(env, workshop_capacity)

    def repair (self, truck):
        """The repair process. It takes a truck process and repairs it."""

        repair_time = #TODO
        yield self.env.timeout(repair_time)


    def maintain (self, truck):
        """The maintain process. It takes a truck process and performs 
        a maintenance."""
        
        maint_time = #TODO
        yield self.env.timeout(maint_time)

    next_id = 1 # for indexing different workshops
    Idle = [] # idle workshops
    Busy = [] # busy workshops
    Queue = [] # trucks waiting to be repaired 
    Ndone = 0 # total amount of repaired trucks 
    def __init__(self,env):
    """ Constructor for the Workshop process"""
        self.env = env
        self.id = Workshop.next_id
        Workshop.next_id += 1
        self.action = env.process(self.run()) 
        Workshop.Idle.append(self) # all workshops start as idle
        self.required = env.event() # the event when this workshop is required by an incoming truck

    def run(self):
    """ The run process. It waits until the workshop is required. 
    Then the workshop works until there are no trucks left in the queue"""
        while True:
            yield self.required # tell the workshop it's been required
            self.required = self.env.event()
            Workshop.Idle.remove(self) 
            Workshop.Busy.append(self)
            while Workshop.Queue != []: 
                truck = Workshop.Queue.pop(0)
                yield self.env.timeout(truck.repair_time) # wait until the repair time has elapsed
                print('Truck # %d was repaired at %d' %(truck.id,self.env.now))
                truck.repair_event.succeed() # tell the truck it has been repaired
                Workshop.Ndone += 1
                truck.fleet.off_trucks.remove(truck) 
                if len(truck.fleet.active_trucks) < truck.fleet.design_number: # whether the repaired truck goes working or stand-by
                    truck.activate_event.succeed() # tell the truck it has become active (working)
                    truck.fleet.active_trucks.append(truck)
                else:
                    truck.fleet.stand_by_trucks.append(truck)
            Workshop.Busy.remove(self) # there are no more trucks in the queue so the workshop becomes idle again
            Workshop.Idle.append(self)
