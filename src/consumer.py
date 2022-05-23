"""
This module represents the Consumer.

"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

        self.place_order = marketplace.place_order
        self.id = marketplace.new_cart
        self.add = marketplace.add_to_cart
        self.remove = marketplace.remove_from_cart
    
    def run(self): 
        # Iterates through list of carts
        for c in self.carts:
            # Current cart's id
            c_id = self.id()
            # Iterates through operations in current cart
            for op in c:
                # Adds/Removes product by specified quantity
                i = 0
                while i < op['quantity']:
                    if op['type'] == 'add':
                        success = self.add(c_id, op['product'])
                    elif op['type'] == 'remove':
                        success = self.remove(c_id, op['product'])
                    # Checks if operation was successful
                    if success == False:
                        time.sleep(self.retry_wait_time)
                    else:
                        i += 1
            # Places order for current cart
            self.place_order(c_id)
