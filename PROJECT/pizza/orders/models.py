import datetime

from django.db import models
from django.utils import timezone

class Pizza(models.Model):
    """A pizza"""
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0) # In cents
    pass

class Topping(models.Model):
    """A Topping"""
    name = models.CharField(max_length=80)
    price = models.IntegerField(default=0) # In cents
    pass

class Address(models.Model):
    """A customer address."""
    street = models.CharField(max_length=200) # Ex: Sample Street 42
    postal_code = models.CharField(max_length=5) # exactly 5 digits
    city = models.CharField(max_length=200)


class Customer(models.Model):
    """A customer. Has a name and an address"""
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Order(models.Model):
    """Models an Order.
    A order consists of a customer receiving the order, a number of pizzas and a set of extra toppings.
    and the date at which the order was created.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    toppings = models.ManyToManyField(Topping)
    received_date = models.DateTimeField('date received')
    
    def is_getting_old(self):
        """Is this order older then 1 hour?"""
        return not self.is_new()

    def is_new(self):
        """Is this order newer then 1 hour?"""
        return self.received_date >= timezone.now() + datetime.timedelta(hours=1)
