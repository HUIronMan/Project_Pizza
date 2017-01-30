"""
Utility functions used by views, factored out to
be accessible by tests.
"""

from .models import *

## Create carts

def create_new_cart():
    new_cart = Cart()
    new_cart.save()
    print("Created new cart with id " + str(new_cart.id))
    return new_cart

def open_or_create_cart(request):
     # Check if we have an open cart
    try:
        cart = request.session['cart_id']
        print("Active cart " + request.session['cart_id'])
        if Cart.objects.filter(pk=int(request.session['cart_id'])).exists():
            cart = Cart.objects.get(pk=int(request.session['cart_id']))
        else:
            # This can happen if the cart was deleted during the session
            cart = __create_new_cart()
            request.session['cart_id'] = str(cart.id)
        return cart
    except KeyError:
        print("No active cart")
        cart = create_new_cart()
        request.session['cart_id'] = str(cart.id)
        request.session.set_expiry(0)
        return cart


def is_cart_open(request):
    if not 'cart_id' in request.session.keys():
        return False
    if not Cart.objects.filter(pk=int(request.session['cart_id'])).exists():
        return False
    return True


def push_pizza_on_cart(cart, menu_pizza_id, size_id, menu_topping_ids):
    """Push a pizza of the given size and additional toppings onto the given cart
    """
    order_pizza = OrderPizza(pizza=MenuPizza.objects.get(pk=menu_pizza_id), cart=cart)
    order_pizza.save()
    size = OrderSize(size=MenuSize.objects.get(pk=size_id), pizza=order_pizza)
    size.save()
    print("Ordered pizza: " + str(order_pizza))
    print("Ordered size: " + str(size))
    for topping in menu_topping_ids:
        top = OrderTopping(topping=MenuTopping.objects.get(pk=topping), pizza=order_pizza)
        top.save()
        print("Ordered topping: " + str(top))

def create_order_from_cart(cart):
    new_order = Order(from_cart=cart, customer_name=request.POST['name'], customer_address=request.POST['addr'])
    new_order.save()
    return new_order


## Some utility functions
