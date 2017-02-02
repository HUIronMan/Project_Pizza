import datetime

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.conf import settings
import importlib
from .models import *

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

    def test_Database(self):
        pass
        return
        #self.assertContains(self.pizza1, "Pizza1")


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


 
class Test_views_py(TestCase):
    """WhiteBoxTesting for views"""

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



    def test_menu_item_size(self):
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

    def test_menu_item(self):
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

    def test_push_on_cart(self):
        # Create an instance of a GET request.
        request = self.factory.post('/', {'topping1': 1, 'topping2': 2,})

        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()

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


#clear cart

#restock
#continue shopping
#add stock

#place order

#check order as cook

#check if order status can be changed

'''the following functions still need tests

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

class Test_models_py(TestCase):
    """WhiteBoxTesting for models"""


'''The following functions still need tests
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

class MenuSize(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField(default=0) # in cents
    ntopings = models.IntegerField(default=3) # number of available toppings
    allows_splitting = models.BooleanField(default=False)

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

    def max_toppings(self):
        return str(self.ntopings)      

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
            s += pizza.ordersize_set.get().name()+"\n"
            for topping in pizza.ordertopping_set.all():
                s += "  " + topping.name() + "\n"
        return s

    def total(self):
        total = 0
        for pizza in self.orderpizza_set.all():
            total += pizza.price()
            total += pizza.ordersize_set.get().price()
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
        return price_str

class OrderPizza(models.Model):
    """A pizza contained in an order."""
    pizza = models.ForeignKey(MenuPizza, on_delete=models.CASCADE, related_name='pizza')
    pizza_half = models.ForeignKey(MenuPizza, on_delete=models.CASCADE, related_name='pizza_half', null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def price(self):
        half_price = 0
        if self.pizza_half:
            half_price = self.pizza_half.price
        return self.pizza.price if self.pizza.price > half_price else self.pizza_half.price

    def readable_price(self):
        """The price in the usual e.cc format"""
        half_price = 0
        if self.pizza_half:
            half_price = self.pizza_half.price
        return self.pizza.readable_price() if self.pizza.price > half_price else self.pizza_half.readable_price()

    def name(self):
        return self.pizza.name if self.pizza_half == None else self.pizza.name + "/" + self.pizza_half.name


    def __str__(self):
        return self.name()

class OrderSize(models.Model):
    """A Size contained in an order. Belongs to a concrete OrderPizza"""
    size = models.ForeignKey(MenuSize, on_delete=models.CASCADE)
    pizza = models.ForeignKey(OrderPizza, on_delete=models.CASCADE)

    def price(self):
        return self.size.price

    def readable_price(self):
        """The price in the usual e.cc format"""
        return self.size.readable_price()

    def name(self):
        return self.size.name

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

'''


class Test_util_py(TestCase):
    """WhiteBoxTesting for models"""

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

    def test_create_new_cart(self):
        new_test_cart = None
        new_test_cart = create_new_cart()
        self.assertNotEqual(new_test_cart, None)

    def test_open_or_create_cart(self):
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()
        new_test_cart = None
        new_test_cart = open_or_create_cart(request) #test except branch
        self.assertNotEqual(new_test_cart, None)
        new_test_cart2 = open_or_create_cart(request)
        self.assertEqual(new_test_cart, new_test_cart2) # test try branch


    def test_is_cart_open(self):
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()
        self.assertEqual(is_cart_open(request),False)
        open_or_create_cart(request)
        self.assertEqual(is_cart_open(request),True)


    def test_push_pizza_on_cart(self):
        #MenuPizza.objects = {"menu_pizza_id": 1}
        push_pizza_on_cart(create_new_cart() , 1, 1, 1, [1])


    def test_create_order_from_cart(self):
        new_cart = create_new_cart()
        push_pizza_on_cart(new_cart , 1, 1, 1, [1])
        new_order = None
        new_order = create_order_from_cart(new_cart, 'pruefer', 'uni')
        self.assertNotEqual(new_order, None)

