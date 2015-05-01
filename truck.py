"""Process that represent a truck entity"""

from workshop import Workshop
class Truck(object):
""" A truck is represented as a process. It has components that 
may fail and thus cause the truck to need reparation. 
Trucks wait for an empty workshop and the for the reparation process to be 
completed. 
Repaired trucks can go either active (working) or stand-by """

    repair_time = 0 # time of last reparation = 0 by default
    def __init__(self,env,id,components,fleet):
	"""" Constructor for the Truck process"""
        self.components = components # list containing all the components of this truck
        self.env = env
        self.id = id
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

    def run(self):
	""" The run process. The truck waits to be activated. Then it works until one of its components
	triggers the fail event and the truck goes off. After this, the truck goes to the Workshop queue 
	and waits until the repair event is triggered. """
        while True:
            yield self.activate_event
            self.activate_event = self.env.event()
            self.standby_time += self.env.now-self.repair_time
            start_time = self.env.now
            print('Truck # %d started working at %d' %(self.id, self.env.now))
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
        print('Truck # %d stopped working at %d' % (self.id, self.env.now))
        if self.fleet.stand_by_trucks != []:
            truck = self.fleet.stand_by_trucks.pop(0)
            truck.activate_event.succeed()
            self.fleet.active_trucks.append(truck)




