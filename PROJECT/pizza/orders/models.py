import datetime

from django.db import models
from django.utils import timezone

"""
We need the following objects:

    Pizzas - A pizza has a name and a price. (TODO: Maybe at description and image?)
             The Model "MenuPizza" acts as both the source for the menu view and
             as a template for "OrderPizza", which can be placed inside an order with
             additional toppings.

    Topping - A Topping can be ordered to be placed on a pizza.
              

    Cart - The customers cart. Contains "OrderPizzas"

    Order - Created from a non-empty cart. Contains a number of OrderPizzas and the customers
            name and address.

"""

class MenuPizza(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0) # in cents

    def __str__(self):
        return self.name

    def readable_price(self):
        """ Returns the price in euros, with 2 cent-digits after the decimal-point """
        price_str = str(self.price / 100.0)
        # find the '.' and add a second 0, if necessary
        for i in range(len(price_str)):
            if price_str[i] != '.':
                continue
            if i >= len(price_str) - 2:
                price_str += "0"
                break
        return price_str

class MenuTopping(models.Model):
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0) # in cents

    def __str__(self):
        return self.name

    def readable_price(self):
        price_str = str(self.price / 100.0)
        # find the '.' and add a second 0, if necessary
        for i in range(len(price_str)):
            if price_str[i] != '.':
                continue
            if i >= len(price_str) - 2:
                price_str += "0"
                break
        return price_str


class Cart(models.Model):
    """
    A temporary customers cart.
    We don't need any data besides the automatically generated ID
    """
    def is_empty(self):
        return len(self.orderpizza_set.all()) == 0

    def __str__(self):
        s = "cart " + str(self.id)
        s += ":\n"
        for pizza in self.orderpizza_set.all():
            s += pizza.name() + "\n"
            for topping in pizza.ordertopping_set.all():
                s += "  " + topping.name() + "\n"
        return s

    def total(self):
        total = 0
        for pizza in self.orderpizza_set.all():
            total += pizza.price()
            for topping in pizza.ordertopping_set.all():
                total += topping.price()
        return total

    def total_readable(self):
        price_str = str(self.total() / 100.0)
        # find the '.' and add a second 0, if necessary
        for i in range(len(price_str)):
            if price_str[i] != '.':
                continue
            if i >= len(price_str) - 2:
                price_str += "0"
                break
        price_str += " €"
        return price_str

class OrderPizza(models.Model):
    """A pizza contained in an order."""
    pizza = models.ForeignKey(MenuPizza, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def price(self):
        return self.pizza.price

    def readable_price(self):
        """The price in the usual e.cc format"""
        return self.pizza.readable_price()

    def name(self):
        return self.pizza.name

    def __str__(self):
        return self.name()

class OrderTopping(models.Model):
    """A Topping contained in an order. Belongs to a concrete OrderPizza"""
    topping = models.ForeignKey(MenuTopping, on_delete=models.CASCADE)
    pizza = models.ForeignKey(OrderPizza, on_delete=models.CASCADE)

    def price(self):
        return self.topping.price

    def readable_price(self):
        """The price in the usual e.cc format"""
        return self.topping.readable_price()

    def name(self):
        return self.topping.name

    def __str__(self):
        return self.name()

class Order(models.Model):
    """A order entered into the system"""
    STATE_NEW = 0
    STATE_BAKING = 1
    STATE_DONE = 2
    
    state = models.SmallIntegerField(default=STATE_NEW)
    from_cart = models.OneToOneField(Cart, on_delete=models.CASCADE, primary_key=False)
    # Since we dont do customer registration,
    # simpy putting the name and address in the Order
    # is probably fine
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    
    def __str__(self):
        state_str = ""
        if self.state == Order.STATE_NEW:
            state_str = "[NEW] "
        elif self.state == Order.STATE_BAKING:
            state_str = "[BAKING] "
        else:
            state_str = "[DONE] "
        return state_str + " %d" % self.from_cart.id

    def pizzas(self):
        return self.from_cart.orderpizza_set.all()
   
    def total(self):
        return self.from_cart.total_readable()
