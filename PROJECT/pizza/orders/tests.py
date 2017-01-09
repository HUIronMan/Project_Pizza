import datetime

from django.test import TestCase
from django.utils import timezone


from .models import Order

# Create your tests here
class OrderMethodTests(TestCase):
    def test_is_getting_old_with_future_order(self):
        """
        Is_getting_old() should return False for orders where received_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(hours=1)
        future_order = Order(received_date=time)
        self.assertIs(future_order.is_getting_old(), False)
