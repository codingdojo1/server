from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def new(req):
  return render(req, 'users/new.html')

def create(req):
  errors = User.objects.validate(req.POST)
  if errors:
    for error in errors:
      messages.error(req, error)
    return redirect('users:new')
  user = User.objects.create_user(req.POST)
  req.session['user_id'] = user.id
  return redirect('products:index')

def login(req):
  valid, result = User.objects.login(req.POST)
  if not valid:
    messages.error(req, result)
    return redirect('users:new')
  else:
    req.session['user_id'] = result.id
  return redirect('products:index')

def logout(req):
  req.session.clear()
  return redirect('users:new')
