from django.db import models
from ..users.models import User
from ..products.models import Product

# Create your models here.
class OrderManager(models.Manager):
  def add_product(self, form_data, user_id):
    # cart is the current order, cart is an Order object
    cart = self.get_active_cart(user_id)
    product = Product.objects.get(id=form_data['product_id'])
    # check to see if order already has at least one of current product attached
    attached_products = cart.order_products.filter(product=product.id)
    print(attached_products)
    if attached_products:
      order_item = attached_products[0]
      order_item.amount += 1
      order_item.save()
    else:
      OrderProduct.objects.create(
        product = product,
        order = cart,
        amount = 1
      )
    product.num_available -= 1
    product.save()
    return

  def get_active_cart(self, user_id):
    active_orders = self.filter(user=user_id).filter(in_progress=False)
    if active_orders:
      cart = active_orders[0]
    else:
      cart = self.create_default_order(user_id)
    return cart

  def create_default_order(self, user_id):
    user = User.objects.get(id=user_id)
    return self.create(
      is_fulfilled = False,
      in_progress = False,
      user = user,
    )

  def place_order(self, order_id, user_id):
    order = self.get(id=order_id)
    order.in_progress = True
    order.save()
    self.create_default_order(user_id)
    return

class Order(models.Model):
  is_fulfilled = models.BooleanField()
  in_progress = models.BooleanField()
  user = models.ForeignKey(User, related_name="orders")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = OrderManager()

class OrderProductManager(models.Manager):
  pass

class OrderProduct(models.Model):
  product = models.ForeignKey(Product, related_name="order_products")
  order = models.ForeignKey(Order, related_name="order_products")
  amount = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
