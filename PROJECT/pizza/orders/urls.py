from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.menu, name='menu'),
    url(r'^(?P<pizza_id>[0-9]+)/$', views.menu_item_size, name='menu_item_size'),
    url(r'^(?P<pizza_id>[0-9]+)/(?P<size_id>[0-9]+)/$', views.menu_item, name='menu_item'),
    url(r'^(?P<pizza_id>[0-9]+)/(?P<size_id>[0-9]+)/push_on_cart/$', views.push_on_cart, name='push_on_cart'),
    url(r'^cart/show$', views.show_cart, name='show_cart'),
    url(r'^cart/clear$', views.clear_cart, name='clear_cart'),
    url(r'^order/confirm$', views.confirm_order, name='confirm_order'),
    url(r'^order/place$', views.place_order, name='place_order'),
    url(r'^order/thanks$', views.thanks, name='thanks'),
    url(r'^staff/open_orders$', views.ShowOpenOrders.as_view(), name='show_open_orders'),
    url(r'^staff/set_order_state/(?P<order_id>[0-9]+)/(?P<state>[0-9]+)/$', views.set_order_state, name='set_order_state')
]
