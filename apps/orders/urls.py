from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^cart/$', views.cart, name="cart"),
  url(r'^add_product/$', views.add_product, name="add_product"),
  url(r'^place_order/$', views.place_order, name="place_order")
]
