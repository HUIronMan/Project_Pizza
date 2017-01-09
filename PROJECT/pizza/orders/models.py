from django.db import models

class Order(models.Model):
    """Models an Order.
    A order consists of a customer receiving the order, a number of pizzas and a set of extra toppings.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza)
    toppings = models.ManyToManyField(Topping)

class Customer(models.Model):
    """A customer. Has a name and an address"""
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Address(models.Model):
    """A customer address."""
    street = models.CharField(max_length=200) # Ex: Sample Street 42
    postal_code = models.CharField(max_length=5) # exactly 5 digits
    city = models.CharField(max_length=200)

class Pizza(models.Model):
    """A pizza"""
    pass

class Topping(models.Model):
    """A Topping"""
    pass
