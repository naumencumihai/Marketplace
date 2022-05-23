"""
This module represents the Producer.

"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        self.id = marketplace.register_producer
        self.publish = marketplace.publish

    def run(self):
        id = self.id()
        products = self.products
        rwt = self.republish_wait_time

        # p[0]: id; p[1]: quantity; p[2]: wait time
        while True:
            for p in products:
                pid = p[0]
                q = p[1]
                wt = p[2]
                i = 0
                # Publishes product by specifeid quantity
                while i < q:
                    success = self.publish(id, pid)

                    # Checks if publish was successful
                    if success == False:
                        # Waits republish_wait_time
                        time.sleep(rwt)
                    else:
                        # waits product-specific wait time
                        time.sleep(wt)
                        i += 1

