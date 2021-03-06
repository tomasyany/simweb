"""This class represents the components inventory."""

class Inventory(object):
    """An inventory has an initial stock for each of the components.

    Each time a component is retrieve from the inventory, it has to be asked
    for reposition. We call this politic one-to-one.
    """

    def __init__(self, env, start_inventory, mon_step):
        self.env = env
        # component is a dictionary where they key indicates the component's
        # type and the value is equal to the initial inventory for this
        # component.
        self.components = {}
        for k, v in start_inventory.items():
            self.components[k] = v

        self.monitor_step = mon_step  # monitoring time step

        # inventory disp stores the amount of components in inventory
        self.inventory_disp = {}
        for k in self.components.keys():
            self.inventory_disp[k] = []

        # inv_breaks stores [# times component was in inventory, # inventory
        # breaks]
        self.inv_breaks = {}
        for name in self.components.keys():
            self.inv_breaks[name] = [0, 0]

        self.monitor_process = self.env.process(self.monitor_inventory())

        # queue is a dictionary where the key indicates the component's type
        # and the value is list of trucks waiting for this component
        self.queue = {}
        for idx in self.components.keys():
            self.queue[idx] = []

    def request_component(self, truck):
        # after a truck fails it will call this method
        c_type = truck.comp_type
        if self.components[c_type] > 0: # if there are componnets left in
        # inventory
            self.components[c_type] -= 1
            self.inv_breaks[c_type][0] += 1
            print('Truck # %d has taken a component of type %s from '
                  'inventory at %f' %(truck.id, c_type, self.env.now))
            truck.got_component.succeed()
        else: #if there are no components in inventory
            self.queue[c_type].append(truck)
            self.inv_breaks[c_type][1] += 1
        # put an replacement order
        # self.env.process(self.put_order(c_type, truck.comp_inventory_time))

    def put_order(self, c_type, time_out):
        yield self.env.timeout(time_out)
        if self.queue[c_type] != []:
            T = self.queue[c_type].pop(0)
            print('Truck # %d has taken a component of type %s from '
                  'inventory at %f' %(T.id, c_type, self.env.now))
            T.got_component.succeed()
        else:
            self.components[c_type] += 1

    def monitor_inventory(self):
        while True:
            for k in self.inventory_disp.keys():
                self.inventory_disp[k].append(self.components[k])

            yield self.env.timeout(self.monitor_step)

    def get_mean_invetory(self):
        output = {}
        for k, v in self.inventory_disp.items():
            output[k] = float(sum(v))/len(v)

        return output