"""This class represents the components inventory."""

from simpy import Container

class Inventory(object):
    """An inventory has an initial stock for each of the components.

    Each time a component is retrieve from the inventory, it has to be asked
    for reposition. We call this politic one-to-one.
    """

    def __init__(self, env, initial_stock, components):
        self.enf = env
        self.stock = [Container(env, capacity=initial_stock)
                        for i in range(components)]

    def add_comp(component_id):
        """Adds 1 component to the stock."""
        self.stock[component_id].put(1)

    def take_comp(component_id):
        self.stock[component_id].put(-1)