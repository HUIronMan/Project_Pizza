import datetime

from django.test import TestCase
from django.utils import timezone


from .models import *
from .views import *
from .util import *

# Create your tests here
class OrderMethodTests(TestCase):
    def test_is_getting_old_with_future_order(self):
        """
        Is_getting_old() should return False for orders where received_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_order = Order(received_date=time)
        self.assertIs(future_order.is_getting_old(), False)


#client test example
def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/url/to/view')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')


class TestPage(TestCase):

   def setUp(self):
       self.client = Client()

   def test_index_page(self):
       url = reverse('index')
       response = self.client.get(url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'index.html')
       self.assertContains(response, 'Company Name XYZ')



 #test models

 class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Entry(title="My entry title")
        self.assertEqual(str(entry), entry.title)
