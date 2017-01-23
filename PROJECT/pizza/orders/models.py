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
    created_on = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        s = "cart " + str(self.id)
        s += ":\n"
        for pizza in OrderPizza.objects.filter(cart__id=self.id):
            s += pizza.name() + "\n"
            for topping in OrderTopping.objects.filter(pizza__id=pizza.id):
                s += "  " + topping.name() + "\n"
        return s

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
