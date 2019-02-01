from django.db import models
from ..users.models import User
from decimal import *

# Create your models here.
class ProductManager(models.Manager):
  def validate(self, form_data):
    errors = []

    if len(form_data['name']) < 2:
      errors.append('Name must be at least 2 characters long.')

    try:
      num_available = int(form_data['num_available'])
      if num_available < 1:
        errors.append('Must have at least 1 item in stock.')
    except:
      errors.append('Items in stock must be a number.')

    try:
      price = Decimal(form_data['price']).quantize(Decimal('.01'), rounding=ROUND_DOWN)
      if price < 0.01:
        errors.append('Product must cost money.')
    except:
      errors.append('Price must be a valid format.')

    if len(form_data['description']) < 1:
      errors.append('Must include a description')

    return errors

  def create_product(self, form_data, user_id):
    price = Decimal(form_data['price']).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    num_available = int(form_data['num_available'])
    user = User.objects.get(id=user_id)
    self.create(
      name=form_data['name'],
      price=price,
      num_available=num_available,
      description=form_data['description'],
      creator=user,
    )

  def update(self, form_data, product_id):
    product = self.get(id=product_id)

    price = Decimal(form_data['price']).quantize(Decimal('.01'), rounding=ROUND_DOWN)

    product.name = form_data['name']
    product.num_available = int(form_data['num_available'])
    product.price = price
    product.description = form_data['description']
    product.save()

class Product(models.Model):
  name = models.CharField(max_length=255)
  num_available = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  creator = models.ForeignKey(User, related_name="products")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = ProductManager()
