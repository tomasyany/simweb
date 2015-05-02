import simpy


class Component(object):
    next_id = 1
    def __init__(self,env,truck,lifetime_distribution,repairtime_distribution,replacement_distribution):
        self.truck = truck
        self.distlife = lifetime_distribution
        self.distrepair = repairtime_distribution
        self.distreplacement = replacement_distribution
        self.env = env
        self.time_left = self.distlife.getInstance()
        self.startTime = env.now
        self.id = Component.next_id
        Component.next_id += 1
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.truck.activate_event
            start_time = self.env.now
            try:
                yield self.env.timeout(self.time_left)
                self.truck.fail_event.succeed()
                self.time_left = self.distlife.getInstance()
                self.truck.comp_inventory_time = self.distreplacement.getInstance()
                self.truck.comp_repair_time = self.distrepair.getInstance()
                for c in self.truck.components:
                    if c.id != self.id:
                        c.action.interrupt()
            except simpy.Interrupt:
                self.time_left -= (self.env.now-start_time)