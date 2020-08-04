from django.shortcuts import render
from . models import Product

def home(request) :
  items = Product.objects.all()
  context = {
    'title' : 'home',
    'items' : items ,
  }
  return render(request, 'home.html' , context)

def product(request):
  items = Product.objects.all()
  return render(request, 'product.html' , {'title':'product','items':items})

