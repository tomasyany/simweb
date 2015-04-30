"""This class represents the components inventory."""

from simpy import Container

class Inventory(object):

    def __init__(self, env, initial_stock, components):
        self.enf = env
        self.stock = [Container(env, capacity=initial_stock)
                        for i in range(components)]

    def add_comp(component_id):
        """Adds 1 component to the stock."""
        self.stock[component_id].put(1)

    def take_comp(component_id):
        self.stock[component_id].put(-1)