class Customer:
    _all = []

    def __init__(self, name):
        self.name = name
        Customer._all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not (1 <= len(value) <= 15):
            raise ValueError("Name must be 1–15 characters.")
        self._name = value

    def orders(self):
        return [order for order in Order._all if order.customer is self]

    def coffees(self):
        return list({order.coffee for order in self.orders()})

    def create_order(self, coffee, price):
        return Order(self, coffee, price)

    @classmethod
    def most_aficionado(cls, coffee):
        customer_spending = {}
        for order in coffee.orders():
            customer_spending[order.customer] = customer_spending.get(order.customer, 0) + order.price
        if not customer_spending:
            return None
        return max(customer_spending, key=customer_spending.get)


class Coffee:
    _all = []

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Coffee name must be a string.")
        if len(name) < 3:
            raise ValueError("Coffee name must be at least 3 characters.")
        self._name = name
        Coffee._all.append(self)

    @property
    def name(self):
        return self._name  # Immutable

    def orders(self):
        return [order for order in Order._all if order.coffee is self]

    def customers(self):
        return list({order.customer for order in self.orders()})

    def num_orders(self):
        return len(self.orders())

    def average_price(self):
        orders = self.orders()
        if not orders:
            return 0
        return sum(order.price for order in orders) / len(orders)


class Order:
    _all = []

    def __init__(self, customer, coffee, price):
        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer instance.")
        if not isinstance(coffee, Coffee):
            raise TypeError("coffee must be a Coffee instance.")
        if not (isinstance(price, float) or isinstance(price, int)):
            raise TypeError("price must be a float.")
        if not (1.0 <= float(price) <= 10.0):
            raise ValueError("price must be between 1.0 and 10.0.")
        self._customer = customer
        self._coffee = coffee
        self._price = float(price)
        Order._all.append(self)

    @property
    def customer(self):
        return self._customer

    @property
    def coffee(self):
        return self._coffee

    @property
    def price(self):
        return self._price  # Immutable

# ...end of file...