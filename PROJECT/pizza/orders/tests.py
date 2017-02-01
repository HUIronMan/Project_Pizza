import datetime

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.conf import settings
import importlib

from .models import *
from .views import *
from .util import *



'''
# Create your tests here
class OrderMethodTests(TestCase):
    def test_is_getting_old_with_future_order(self):
        """
        Is_getting_old() should return False for orders where received_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_order = Order(received_date=time)
        self.assertIs(future_order.is_getting_old(), False)
'''

class TestDB(TestCase):
  """Idea setup a customer order in a database only and see if it is viewable in the end"""

  def setUp(self):
    self.client = Client()

  @classmethod
  def setUpTestData(cls):
    cls.pizza1 = MenuPizza.objects.create(name="Pizza1", price=100)
    cls.pizza2 = MenuPizza.objects.create(name="Pizza2", price=1000)
    cls.size1  = MenuSize.objects.create(name="size1", price=100, ntopings=1, allows_splitting=False)
    cls.size2  = MenuSize.objects.create(name="size2", price=1000, ntopings=2, allows_splitting=True)
    cls.topping1 = MenuTopping.objects.create(name = "topping1", price = 100) # in cents
    cls.topping2 = MenuTopping.objects.create(name = "topping2", price = 1000) # in cents
    cls.cart1 = Cart.objects.create() # in cents
    cls.cart2 = Cart.objects.create() # in cents

  def TestDatabase(self):
    self.assertContains(self.pizza1, "Pizza1")


'''
class OrderPizza(models.Model):
    """A pizza contained in an order."""
    pizza = models.ForeignKey(MenuPizza, on_delete=models.CASCADE, related_name='pizza')
    pizza_half = models.ForeignKey(MenuPizza, on_delete=models.CASCADE, related_name='pizza_half', null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
class OrderSize(models.Model):
    """A Size contained in an order. Belongs to a concrete OrderPizza"""
    size = models.ForeignKey(MenuSize, on_delete=models.CASCADE)
    pizza = models.ForeignKey(OrderPizza, on_delete=models.CASCADE)
class OrderTopping(models.Model):
    """A Topping contained in an order. Belongs to a concrete OrderPizza"""
    topping = models.ForeignKey(MenuTopping, on_delete=models.CASCADE)
    pizza = models.ForeignKey(OrderPizza, on_delete=models.CASCADE)
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
'''





class TestWebInterface(TestCase):
  """BlackBoxTesting"""

  def setUp(self):
    self.client = Client()

  @classmethod
  def setUpTestData(cls):
    cls.pizza1 = MenuPizza.objects.create(name="Pizza1", price=100)
    cls.pizza2 = MenuPizza.objects.create(name="Pizza2", price=1000)
    cls.size1  = MenuSize.objects.create(name="size1", price=100, ntopings=1, allows_splitting=False)
    cls.size2  = MenuSize.objects.create(name="size2", price=1000, ntopings=2, allows_splitting=True)
    cls.topping1 = MenuTopping.objects.create(name = "topping1", price = 100) # in cents
    cls.topping2 = MenuTopping.objects.create(name = "topping2", price = 1000) # in cents

  def test_404(self):
    url = '/somethingNotExisting'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)

  def test_menu_page(self):
    url = '/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'orders/menu.html')
    self.assertNotContains(response, 'Sorry, our menu is currently empty :-(')
    self.assertNotContains(response, 'My cart')
    self.assertContains(response, 'Pizza1')
    self.assertContains(response, 'Pizza2')

  def test_size_page(self):
    url = '/1/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'orders/menu_item_size.html')
    self.assertNotContains(response, "Sorry, we currently don't have any sizes.")
    self.assertContains(response, 'size1')
    self.assertContains(response, 'size2')
    self.assertContains(response, 'Pizza1')
    url = '/2/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'orders/menu_item_size.html')
    self.assertNotContains(response, "Sorry, we currently don't have any sizes.")
    self.assertContains(response, 'size1')
    self.assertContains(response, 'size2')
    self.assertContains(response, 'Pizza2')

  def test_toppings_page(self):
    url = '/1/1/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'orders/menu_item.html')
    self.assertNotContains(response, "Sorry, we don't have any additional toppings.")
    self.assertContains(response, 'topping1')
    self.assertContains(response, 'topping2')
    self.assertContains(response, 'Pizza1')
    url = '/2/2/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'orders/menu_item.html')
    self.assertNotContains(response, "Sorry, we don't have any additional toppings.")
    self.assertContains(response, 'topping1')
    self.assertContains(response, 'topping2')
    self.assertContains(response, 'Pizza1') #is pizza splitting possible
    self.assertContains(response, 'Pizza2')

  def test_order_confirmation_page(self):
    url = '/1/1/push_on_cart/'
    response = self.client.post(url, {'topping1': 1, 'topping2': 2,})
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/show', status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
    response = self.client.get('/cart/show')
    self.assertEqual(response.status_code, 200)    
    self.assertContains(response, 'topping1')
    self.assertContains(response, 'topping2')
    self.assertContains(response, 'Pizza1')
    url = '/2/2/push_on_cart/'
    response = self.client.post(url, {'topping1': 1, 'pizza1': 1})
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, '/cart/show', status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
    response = self.client.get('/cart/show')
    self.assertEqual(response.status_code, 200)   
    self.assertContains(response, 'topping1')
    self.assertContains(response, 'Pizza1') #is pizza splitting possible
    self.assertContains(response, 'Pizza2')

#clear cart

#restock
#continue shopping
#add stock

#place order

#check order as cook

#check if order status can be changed


 
class TestSubroutinesWithoutWebinterface(TestCase):
    """WhiteBoxTesting"""

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.pizza1 = MenuPizza.objects.create(name="Pizza1", price=100)
        cls.pizza2 = MenuPizza.objects.create(name="Pizza2", price=1000)
        cls.size1  = MenuSize.objects.create(name="size1", price=100, ntopings=1, allows_splitting=False)
        cls.size2  = MenuSize.objects.create(name="size2", price=1000, ntopings=2, allows_splitting=True)
        cls.topping1 = MenuTopping.objects.create(name = "topping1", price = 100) # in cents
        cls.topping2 = MenuTopping.objects.create(name = "topping2", price = 1000) # in cents


    def test_menu(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.session = {}

        response = menu(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Sorry, our menu is currently empty :-(')
        self.assertNotContains(response, 'My cart')
        self.assertContains(response, 'Pizza1')
        self.assertContains(response, 'Pizza2')



    def test_size_page(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.session = {}

        response =  menu_item_size(request, 1)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sorry, we currently don't have any sizes.")
        self.assertContains(response, 'size1')
        self.assertContains(response, 'size2')
        self.assertContains(response, 'Pizza1')

        response = menu_item_size(request, 2)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sorry, we currently don't have any sizes.")
        self.assertContains(response, 'size1')
        self.assertContains(response, 'size2')
        self.assertContains(response, 'Pizza2')

    def test_toppings_page(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.session = {}

        response = menu_item(request, 1, 1)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sorry, we don't have any additional toppings.")
        self.assertContains(response, 'topping1')
        self.assertContains(response, 'topping2')
        self.assertContains(response, 'Pizza1')
            
        response = menu_item(request, 2, 2)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Sorry, we don't have any additional toppings.")
        self.assertContains(response, 'topping1')
        self.assertContains(response, 'topping2')
        self.assertContains(response, 'Pizza1') #is pizza splitting possible
        self.assertContains(response, 'Pizza2')

    def test_order_confirmation_page(self):
        # Create an instance of a GET request.
        request = self.factory.post('/', {'topping1': 1, 'topping2': 2,})

        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session .save()

        response = push_on_cart(request, 1, 1)
        self.assertEqual(response.status_code, 302)
        '''
        self.assertRedirects(response, '/cart/show', status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
        response = self.client.get('/cart/show')
        self.assertEqual(response.status_code, 200)    
        self.assertContains(response, 'topping1')
        self.assertContains(response, 'topping2')
        self.assertContains(response, 'Pizza1')
        url = '/2/2/push_on_cart/'
        response = self.client.post(url, {'topping1': 1, 'pizza1': 1})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/show', status_code=302, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)
        response = self.client.get('/cart/show')
        self.assertEqual(response.status_code, 200)   
        self.assertContains(response, 'topping1')
        self.assertContains(response, 'Pizza1') #is pizza splitting possible
        self.assertContains(response, 'Pizza2')
        '''


'''
#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import MenuPizza, MenuTopping, Cart, OrderPizza, OrderTopping, Order, MenuSize, OrderSize
from .util import *

# Helper functions for managing the cart







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
    half_pizza_id = None
    if 'half_pizza' in request.POST:
        half_pizza_id = int(request.POST['half_pizza'])

    # Check if we have an open cart or create a new one
    customer_cart = open_or_create_cart(request)

    # Push the selected pizza and toppings onto the cart
    push_pizza_on_cart(customer_cart, pizza_id, half_pizza_id, size_id, toppings)

    return HttpResponseRedirect('/cart/show')

def show_cart(request): 
    customer_cart = open_or_create_cart(request)
    if customer_cart.is_empty():
        context = { 'is_empty': True, 'pizzas': None }
        return render(request, 'orders/show_cart.html', context)
    else:
        pizzas = OrderPizza.objects.filter(cart__id=customer_cart.id)
        context = { 'is_empty': False, 'pizzas': pizzas }
        return render(request, 'orders/show_cart.html', context)

def clear_cart(request):
    if is_cart_open(request):
       del request.session['cart_id']
    return HttpResponseRedirect('/')

def confirm_order(request):
    """Show a form asking for the clients name and address"""
    cart = None
    if is_cart_open(request):
        cart = open_or_create_cart(request)
    else:
        return HttpResponseRedirect('/') # Prevent empty orders
    return render(request, 'orders/confirm_order.html', {'cart': cart, 'total': cart.total_readable()})

def place_order(request):
    if not is_cart_open(request):
        return HttpResponseRedirect('/') # Prevent empty orders
    cart = open_or_create_cart(request)
    new_order = create_order_from_cart(cart, request.POST['name'], request.POST['addr']) 
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

'''