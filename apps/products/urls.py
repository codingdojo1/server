
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^new/$', views.new, name="new"),
  url(r'^create/$', views.create, name="create"),
  url(r'^show/(?P<product_id>\d+)/$', views.show, name="show"),
  url(r'^edit/(?P<product_id>\d+)/$', views.edit, name="edit"),
  url(r'^update/(?P<product_id>\d+)/$', views.update, name="update"),
  url(r'^delete/(?P<product_id>\d+)/$', views.delete, name="delete"),
]
