#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import MenuPizza, MenuTopping, Cart, OrderPizza, OrderTopping

# Create your views here.

class MenuView(generic.ListView):
    """Display the list of offered pizzas"""
    template_name = 'orders/menu.html'
    context_object_name = 'available_pizzas'

    def get_queryset(self):
        return MenuPizza.objects.all()

def menu_item(request, pizza_id): 
    pizza = get_object_or_404(MenuPizza, pk=pizza_id)
    available_toppings = MenuTopping.objects.all()
    return render(request, 'orders/menu_item.html', {'pizza': pizza, 'available_toppings': available_toppings})

def __create_new_cart():
    new_cart = Cart(created_on=timezone.now())
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


def push_on_cart(request, pizza_id):
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
    print("Ordered pizza: " + str(pizza))
    for topping in toppings:
        top = OrderTopping(topping=topping, pizza=pizza)
        top.save()
        print("Ordered topping: " + str(top))

    return HttpResponseRedirect('/cart/show')

def show_cart(request): 
    customer_cart = __open_or_create_cart(request)
    is_empty = not OrderPizza.objects.filter(cart__id=customer_cart.id).exists() 
    if is_empty:
        context = { 'is_empty': is_empty, 'pizzas': None }
        return render(request, 'orders/show_cart.html', context)
    else:
        pizzas = OrderPizza.objects.filter(cart__id=customer_cart.id)
        context = { 'is_empty': is_empty, 'pizzas': pizzas }
        return render(request, 'orders/show_cart.html', context)

def clear_cart(request):
    customer_cart = __open_or_create_cart(request)
    customer_cart.delete()
    return HttpResponseRedirect('/')
