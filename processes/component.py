""" This class describes a component as a process.
"""

import simpy

class Component(object):
    """ This class is useful to define a component as an object
    characeterized by three random time variables (lifetime, repair time and
    inventory replacement time) and by a parent truck.

    Each component has a run() process that waits until its lifetime is over
    and then it tells the parent truck it has failed. However the run()
    process of a component may be interrupted when another component of the
    same parent truck has failed. In this case the run() process won't be
    resumed until the parent truck has been repaired.
    """

    next_id = 1
    def __init__(self,env,truck,lifetime_distribution,repairtime_distribution,
                 replacement_distribution, component_type):
        """The constructor of the Component class."""
        self.truck = truck    # The parent truck

        # The following are objects of the random generator class and they
        # are used to get random instances of the lifetime, repair time and
        # the inventorty replacement time.
        self.distlife = lifetime_distribution
        self.distrepair = repairtime_distribution
        self.distreplacement = replacement_distribution

        self.env = env    # the simpy environment

        # time_left is the remaining lifetime of the component. It is
        # initialized as a random instance of the lifetime distribution
        self.time_left = self.distlife.getInstance()

        self.id = Component.next_id    # Assign a diferent id to each component
        Component.next_id += 1

        # We tell simpy to add this component's run() process
        self.action = env.process(self.run())

        #Component type is an integer that defines the kind of component
        self.type = component_type

    def run(self):
        """
        The run() process.
        1) it waits until the parent truck has been activated

        2) It waits un amount of time equals to time_left

        3) It triggers the fail event corresponding to its parent truck (so
        the parent truck stops working), sets time_left to a new random value
        and tells the parent truck what are the inventory replacement and repair
        times. Finally interrupt all the parent truck's components.

        3') If 2) is interrupted then set time_left is updated.
        """
        while True:
            # Step 1: wait until the parent truck has been activated
            yield self.truck.activate_event
            start_time = self.env.now

            # Step 2
            try:
                # wait time_left
                yield self.env.timeout(self.time_left)
                print('Component # %d of Truck # %d has failed at %d' %(
                    self.id, self.truck.id, self.env.now))
                self.truck.fail_event.succeed()    # Trigger the fail event
                # set time_left to a new random value
                self.time_left = self.distlife.getInstance()

                self.truck.comp_inventory_time = self.distreplacement.getInstance()
                self.truck.comp_repair_time = self.distrepair.getInstance()
                self.truck.comp_type = self.type

                for c in self.truck.components:    # interrupt all components
                    if c.id != self.id:
                        c.action.interrupt()
            except simpy.Interrupt:    # if interrupted, just update time_left
                self.time_left -= (self.env.now-start_time)