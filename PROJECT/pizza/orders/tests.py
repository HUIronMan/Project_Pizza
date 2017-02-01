import datetime

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone


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
  """setup an order through the webpage and check all steps on the way"""

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

#continue shopping

#place order

#check order as cook

#check if order status can be changed


#Hier würde ich gerne die die funktionen ohne webinterface testen, aber das request object hat keine seasson id  
"""
class TestSubroutinesWithoutWebinterface(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')

        # Test my_view() as if it were deployed at /customer/details
        response = menu(request)
        self.assertEqual(response.status_code, 200)
"""