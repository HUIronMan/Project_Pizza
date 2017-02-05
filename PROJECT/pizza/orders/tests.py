import datetime

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.conf import settings
from django.http.response import Http404
import importlib

from .models import *
from .views import *
from .util import *



 
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

        request = self.factory.post('/', {'topping1': 1, 'topping2': 2, 'half_pizza': 2})

        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()

        response = push_on_cart(request, 2, 2)
        self.assertEqual(response.status_code, 302)


    def test_show_cart(self): 
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()

        response = show_cart(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty")
        self.assertNotContains(response, 'topping1')
        self.assertNotContains(response, 'Pizza1')


    def test_clear_cart(self):
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()

        response = clear_cart(request)
        self.assertEqual(response.status_code, 302)

    def test_thanks(self):
        request = self.factory.get('/')
        response = thanks(request)
        self.assertContains(response, 'Thank you for your order')

    def test_get_queryset(self):#
        returnVal = None
        returnVal = ShowOpenOrders.get_queryset(ShowOpenOrders)
        self.assertNotEqual(returnVal, None)


    def test_confirm_order(self):
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        request.session.save()
        cart = open_or_create_cart(request)
        self.assertNotEqual(cart, None)

        response = confirm_order(request)
        self.assertEqual(response.status_code, 200)

    def test_place_order(self):
        request = self.factory.get('/')
        engine = importlib.import_module(settings.SESSION_ENGINE)
        request.session  = engine.SessionStore()
        request.session.save()
        response = clear_cart(request)
        self.assertEqual(response.status_code, 302)

    def test_set_order_state(self):
        request = self.factory.get('/')
        try:
            response = set_order_state(request, -42, 42)
        except Http404:
            self.assertTrue(True)
            return
        self.assertTrue(False)

class Test_models_py(TestCase):
    """WhiteBoxTesting for models"""

   # def setUp(self):
        
        #self.orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=create_new_cart())

    @classmethod
    def setUpTestData(cls): 
        cls.pizza1 = MenuPizza.objects.create(name="Pizza1", price=760)
        cls.pizza2 = MenuSize.objects.create(name="Pizza2", price=123, ntopings=3)
        cls.pizza3 = MenuSize.objects.create(name="Pizza3", price=123, ntopings=5, allows_splitting=True)
        cls.topping1 = MenuTopping.objects.create(name="Topping1", price=321)
        cls.pizza5 = MenuPizza.objects.create(name="Pizza5", price=690)

    def test_menu_pizza_str(self):
        name = MenuPizza.__str__(self.pizza1)
        self.assertEqual(name, "Pizza1")  

    def test_menu_pizza_readable_price(self):
        price = MenuPizza.readable_price(self.pizza1)
        self.assertEqual(price, "7.60")

    def test_menu_size_str(self):
        name2 = MenuSize.__str__(self.pizza2)
        name3 = MenuSize.__str__(self.pizza3)
        self.assertEqual(name2, "Pizza2") 
        self.assertEqual(name3, "Pizza3") 

    def test_menu_size_readable_price(self):
        price = MenuSize.readable_price(self.pizza2)
        self.assertEqual(price, "1.23")         

    def test_max_toppings(self):
        max_toppings_1 = MenuSize.max_toppings(self.pizza2)
        max_toppings_2 = MenuSize.max_toppings(self.pizza3)

        self.assertEqual(max_toppings_1, "3")
        self.assertEqual(max_toppings_2, "5")

    def test_menu_toppings_str(self):
        name4 = MenuTopping.__str__(self.topping1)
        self.assertEqual(name4, self.topping1.name)    

    def test_menu_size_readable_price(self):
        price = MenuTopping.readable_price(self.topping1)
        self.assertEqual(price, "3.21") 

    def test_cart_is_empty(self):
        new_cart = create_new_cart()
        self.assertEqual(Cart.is_empty(new_cart), True)

        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        self.assertEqual(Cart.is_empty(new_cart), False)

    def test_cart_str_(self):
        new_cart = create_new_cart()
        string1 = "cart " + str(new_cart.id) + ":\n"
        self.assertEqual(Cart.__str__(new_cart), string1)

        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        string2 = "cart " + str(new_cart.id)
        string2 += ":\n"
        for pizza in new_cart.orderpizza_set.all():
            string2 += pizza.name() + "\n"
            string2 += pizza.ordersize_set.get().name()+"\n"
            for topping in pizza.ordertopping_set.all():
                string2 += "  " + topping.name() + "\n"
        self.assertEqual(Cart.__str__(new_cart), string2)

        #Todo Create Order with Toppings, test Toppings String

    def test_cart_total(self):
        new_cart = create_new_cart()
        self.assertEqual(Cart.total(new_cart), 0)
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        price = self.pizza2.price + (self.pizza5.price if self.pizza5.price > self.pizza1.price else self.pizza1.price)
        self.assertEqual(Cart.total(new_cart), price)
        #Todo Create Order with Toppings, test Toppings String
    def test_cart_total_readable(self):
        new_cart = create_new_cart()
        self.assertEqual(Cart.total_readable(new_cart), "0.00")
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        odrersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        self.assertEqual(Cart.total_readable(new_cart), "8.83")

    def test_order_pizza_price(self):
        new_cart = create_new_cart()
        orderpizza1 = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        self.assertEqual(OrderPizza.price(orderpizza1), self.pizza1.price);
        orderpizza2 = OrderPizza.objects.create(pizza=self.pizza5, pizza_half=self.pizza1, cart=new_cart)
        self.assertEqual(OrderPizza.price(orderpizza2), self.pizza1.price);

    def test_order_pizza_readable_price(self):
        new_cart = create_new_cart()
        orderpizza1 = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        self.assertEqual(OrderPizza.readable_price(orderpizza1), "7.60");
        orderpizza2 = OrderPizza.objects.create(pizza=self.pizza5, pizza_half=self.pizza1, cart=new_cart)
        self.assertEqual(OrderPizza.readable_price(orderpizza2), "7.60");

    def test_order_pizza_name(self):
        new_cart = create_new_cart()
        orderpizza1 = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=None, cart=new_cart)
        self.assertEqual(OrderPizza.name(orderpizza1), self.pizza1.name);
        orderpizza2 = OrderPizza.objects.create(pizza=self.pizza5, pizza_half=self.pizza1, cart=new_cart)
        self.assertEqual(OrderPizza.name(orderpizza2), self.pizza5.name + "/" + self.pizza1.name);

    def test_order_pizza_str(self):
        new_cart = create_new_cart()
        orderpizza1 = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=None, cart=new_cart)
        self.assertEqual(OrderPizza.__str__(orderpizza1), self.pizza1.name);
        orderpizza2 = OrderPizza.objects.create(pizza=self.pizza5, pizza_half=self.pizza1, cart=new_cart)
        self.assertEqual(OrderPizza.__str__(orderpizza2), self.pizza5.name + "/" + self.pizza1.name);


    def test_order_size_price(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        self.assertEqual(OrderSize.price(ordersize), self.pizza2.price)

    def test_order_size_readable_price(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        self.assertEqual(OrderSize.readable_price(ordersize), "1.23")

    def test_order_size_name(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        self.assertEqual(OrderSize.name(ordersize), self.pizza2.name) 

    def test_order_size_str(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        self.assertEqual(OrderSize.__str__(ordersize), self.pizza2.name)     

    def test_order_topping_price(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        self.assertEqual(OrderTopping.price(ordertoppings), self.topping1.price)

    def test_order_topping_redable_price(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        self.assertEqual(OrderTopping.readable_price(ordertoppings), "3.21")

    def test_order_topping_name(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        self.assertEqual(OrderTopping.name(ordertoppings), self.topping1.name) 

    def test_order_topping_str(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        self.assertEqual(OrderTopping.__str__(ordertoppings), self.topping1.name)

    def test_order_str(self):
        new_cart1 = create_new_cart()
        new_cart2 = create_new_cart()
        new_cart3 = create_new_cart()
        order_new = Order.objects.create(from_cart=new_cart1, customer_name="Pipi Langstrumpf", customer_address="Rudower Chaussee 25")
        self.assertEqual(Order.__str__(order_new), "[NEW] %d" % new_cart1.id)
        order_new = Order.objects.create(state=Order.STATE_BAKING, from_cart=new_cart2, customer_name="Pipi Langstrumpf", customer_address="Rudower Chaussee 25")
        self.assertEqual(Order.__str__(order_new), "[BAKING] %d" % new_cart2.id)
        order_new = Order.objects.create(state=Order.STATE_DONE, from_cart=new_cart3, customer_name="Pipi Langstrumpf", customer_address="Rudower Chaussee 25")
        self.assertEqual(Order.__str__(order_new), "[DONE] %d" % new_cart3.id)    

    def test_order_pizzas(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        order_new = Order.objects.create(from_cart=new_cart, customer_name="Pipi Langstrumpf", customer_address="Rudower Chaussee 25")
        query = Order.pizzas(order_new)
        self.assertEqual(len(query), 1)
        self.assertTrue(orderpizza  in query)

    def test_order_total(self):
        new_cart = create_new_cart()
        orderpizza = OrderPizza.objects.create(pizza=self.pizza1, pizza_half=self.pizza5, cart=new_cart)
        ordersize = OrderSize.objects.create(size=self.pizza2, pizza=orderpizza)
        ordertoppings = OrderTopping.objects.create(topping=self.topping1, pizza=orderpizza)
        order_new = Order.objects.create(from_cart=new_cart, customer_name="Pipi Langstrumpf", customer_address="Rudower Chaussee 25")
        self.assertEqual(Order.total(order_new), "12.04")

class Test_util_py(TestCase):
    """WhiteBoxTesting for util"""

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

