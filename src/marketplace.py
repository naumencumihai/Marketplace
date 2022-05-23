"""
This module represents the Marketplace.

"""

from threading import currentThread, Lock


class MaxLengthQueue(object):
    """
    Class used to represent a producer's queue
    """
    def __init__(self, max_length):
        self.max_length = max_length
        self.queue = []

    def push(self, element):
        self.queue.append(element)

    def push_if_not_full(self, element):
        if len(self.queue) == self.max_length:
            return False
        self.queue.append(element)
        return True

    def pop(self, element):
        if element in self.queue:
            self.queue.remove(element)
            return True
        return False

    def get_queue(self):
        return self.queue


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # Dict to hold producers' queues
        self.producers = {}
        self.producer_lock = Lock()

        # Dict to hold consumers' carts
        self.carts = {}
        self.cart_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Maximum allowed length of a producer's queue
        max_length = self.queue_size_per_producer
        # Allocs queue for current producer and returns it's id
        with self.producer_lock:
            producer_id = len(self.producers)
            self.producers[producer_id] = MaxLengthQueue(max_length)
            return producer_id


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace
        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Current producer's queue
        producer_queue = self.producers[producer_id]
        # Publishes product only if queue not full
        success = producer_queue.push_if_not_full(product)
        if success == False:
            return False
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        # Allocs list for current cart and return it's id
        with self.cart_lock:
            cart_id = len(self.carts)
            self.carts[cart_id] = []
            return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again
        """
        producers = self.producers

        # Current consumer's cart
        cart = self.carts[cart_id]

        # Total number of producers
        no_of_producers = len(producers)

        for current_producer in range(no_of_producers):
            # If current producer has desired product, adds it to cart
            # and removes it from producer's queue
            if producers[current_producer].pop(product):
                cart.append({'product':product, 'producer_id': current_producer})
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        # Current consumer's cart
        cart = self.carts[cart_id]

        # Removes product from cart and returns it to
        # respective producer's queue
        for this in cart:
            if this['product'] == product:
                cart.remove(this)
                producer_id = this['producer_id']
                break
        self.producers[producer_id].push(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        # Current consumer's cart
        cart = self.carts[cart_id]
        # List of products in cart
        products = []
        for this in cart:
            products.append(this['product'])

        # Output order's details
        for product in products:
            print("{0} bought {1}".format(currentThread().getName(), product))
        return products