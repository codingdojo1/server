from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Product
from ..users.models import User

# Create your views here.
def index(req):
  if 'user_id' not in req.session:
    return redirect('users:new')

  context = {
    'purchasable_products': Product.objects.exclude(creator=req.session['user_id']).exclude(num_available__lte=0),
    'user': User.objects.get(id=req.session['user_id']),
  }
  return render(req, 'products/index.html', context)

def new(req):
  return render(req, 'products/new.html')

def show(req, product_id):
  if 'user_id' not in req.session:
    return redirect('users:new')

  try:
    context = {
      'product': Product.objects.get(id=product_id)
    }
  except ObjectDoesNotExist:
    return redirect('products:index')

  return render(req, 'products/show.html', context)

def edit(req, product_id):
  if 'user_id' not in req.session:
    return redirect('users:new')

  # TODO - Implement validation so only owners of the product can access the edit page.

  try:
    context = {
      'product': Product.objects.get(id=product_id)
    }
  except ObjectDoesNotExist:
    return redirect('products:index')

  return render(req, 'products/edit.html', context)

def create(req):
  errors = Product.objects.validate(req.POST)
  if errors:
    for error in errors:
      messages.error(req, error)
    return redirect('products:new')
  # create the product if there are no errors
  Product.objects.create_product(req.POST, req.session['user_id'])
  return redirect('products:index')

def update(req, product_id):
  errors = Product.objects.validate(req.POST)
  if errors:
    for error in errors:
      messages.error(req, error)
    return redirect('products:edit', product_id=product_id)

  Product.objects.update(req.POST, product_id)
  return redirect('products:index')

def delete(req, product_id):
  try:
    product = Product.objects.get(id=product_id)
    product.delete()
  except ObjectDoesNotExist:
    print('TRIED TO DELETE PRODUCT #{}, DOES NOT EXIST'.format(product_id))
  return redirect('products:index')
