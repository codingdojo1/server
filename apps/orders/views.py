from django.shortcuts import render, redirect
from .models import Order

# Create your views here.
def index(req):
  context = {
    'orders': Order.objects.filter(user=req.session['user_id']).filter(in_progress=True)
  }
  return render(req, 'orders/index.html', context)

def cart(req):
  cart = Order.objects.filter(user=req.session['user_id']).filter(
      in_progress=False)[0]
  clean_data = []
  total = 0
  for order_product in cart.order_products.all():
    item = {
      'item': order_product.product.name,
      'price': order_product.product.price,
      'amount': order_product.amount,
      'subtotal': order_product.amount * order_product.product.price
    }
    total += item['subtotal']
    clean_data.append(item)

  context = {
    'cart': clean_data,
    'total': total,
    'order_id': cart.id
  }
  return render(req, 'orders/cart.html', context)

def add_product(req):
  Order.objects.add_product(req.POST, req.session['user_id'])
  return redirect('products:index')

def place_order(req):
  Order.objects.place_order(req.POST['order_id'], req.session['user_id'])
  return redirect('orders:index')
