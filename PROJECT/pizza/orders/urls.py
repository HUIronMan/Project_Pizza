from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.MenuView.as_view(), name='menu'),
    url(r'^(?P<pizza_id>[0-9]+)/$', views.menu_item, name='menu_item'),
    url(r'^(?P<pizza_id>[0-9]+)/push_on_cart/$', views.push_on_cart, name='push_on_cart'),
    url(r'^cart/show$', views.show_cart, name='show_cart'),
    url(r'^cart/clear$', views.clear_cart, name='clear_cart')
]
