#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import MenuPizza, MenuTopping, Cart, OrderPizza, OrderTopping, Order, MenuSize, OrderSize

# Helper functions for managing the cart
def __create_new_cart():
    new_cart = Cart()
    new_cart.save()
    print("Created new cart with id " + str(new_cart.id))
    return new_cart

def __open_or_create_cart(request):
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
        cart = __create_new_cart()
        request.session['cart_id'] = str(cart.id)
        request.session.set_expiry(0)
        return cart


def __is_cart_open(request):
    if not 'cart_id' in request.session.keys():
        return False
    if not Cart.objects.filter(pk=int(request.session['cart_id'])).exists():
        return False
    return True



def menu(request):
    """Display the list of offered pizzas"""
    pizzas = MenuPizza.objects.all()
    customer_cart = None
    if __is_cart_open(request):
        customer_cart = __open_or_create_cart(request)
    context = { 'available_pizzas': pizzas, 'cart': customer_cart }
    return render(request, 'orders/menu.html', context)

        
def menu_item_size(request, pizza_id): 
    pizza = get_object_or_404(MenuPizza, pk=pizza_id)
    available_sizes = MenuSize.objects.all()
    return render(request, 'orders/menu_item_size.html', {'pizza': pizza, 'available_sizes': available_sizes})
  

def menu_item(request, pizza_id, size_id): 
    pizza = get_object_or_404(MenuPizza, pk=pizza_id)
    size  = get_object_or_404(MenuSize, pk=size_id)
    available_toppings = MenuTopping.objects.all()
    return render(request, 'orders/menu_item.html', {'pizza': pizza, 'size': size, 'available_toppings': available_toppings})

def push_on_cart(request, pizza_id, size_id):
    collected_toppings = False
    toppings = []
    i = 1
    while not collected_toppings:
        key = "topping" + str(i)
        if key in request.POST:
            print(key + " is in toppings")
            toppings.append(request.POST["topping" + str(i)])
            i += 1
        else:
            print(key + " is not in toppings")
            collected_toppings = True
    # replace toppings[i] with the referenced topping object
    for i in range(len(toppings)):
        toppings[i] = MenuTopping.objects.get(pk=int(toppings[i]))

    # Check if we have an open cart or create a new one
    customer_cart = __open_or_create_cart(request)

    # Push the selected pizza and toppings onto the cart
    pizza = OrderPizza(pizza=MenuPizza.objects.get(pk=pizza_id), cart=customer_cart)
    pizza.save()
    size = OrderSize(size=MenuSize.objects.get(pk=size_id), pizza=pizza)
    size.save()
    print("Ordered pizza: " + str(pizza))
    print("Ordered size: " + str(size))
    for topping in toppings:
        top = OrderTopping(topping=topping, pizza=pizza)
        top.save()
        print("Ordered topping: " + str(top))

    return HttpResponseRedirect('/cart/show')

def show_cart(request): 
    customer_cart = __open_or_create_cart(request)
    if customer_cart.is_empty():
        context = { 'is_empty': True, 'pizzas': None }
        return render(request, 'orders/show_cart.html', context)
    else:
        pizzas = OrderPizza.objects.filter(cart__id=customer_cart.id)
        context = { 'is_empty': False, 'pizzas': pizzas }
        return render(request, 'orders/show_cart.html', context)

def clear_cart(request):
    if __is_cart_open(request):
       del request.session['cart_id']
    return HttpResponseRedirect('/')

def confirm_order(request):
    """Show a form asking for the clients name and address"""
    cart = None
    if __is_cart_open(request):
        cart = __open_or_create_cart(request)
    else:
        return HttpResponseRedirect('/') # Prevent empty orders
    return render(request, 'orders/confirm_order.html', {'cart': cart, 'total': cart.total_readable()})

def place_order(request):
    if not __is_cart_open(request):
        return HttpResponseRedirect('/') # Prevent empty orders
    cart = __open_or_create_cart(request)
    new_order = Order(from_cart=cart, customer_name=request.POST['name'], customer_address=request.POST['addr'])
    new_order.save()
    print("Created order " + str(new_order))
    return HttpResponseRedirect('/order/thanks')

def thanks(request):
    return render(request, 'orders/thanks.html', {})


class ShowOpenOrders(generic.ListView):
    template_name = 'orders/show_open_orders.html'
    context_object_name = 'open_orders'

    def get_queryset(self):
        """Return all unfinished orders"""
        print(Order.objects.all())
        return Order.objects.exclude(state=Order.STATE_DONE)

def set_order_state(request, order_id, state):
    order = get_object_or_404(Order, pk=order_id)
    order.state = state
    order.save()
    return HttpResponseRedirect('/staff/open_orders')
