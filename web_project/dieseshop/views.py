from django.shortcuts import render , redirect , get_object_or_404
from . models import Category , Product , Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home (request , category_slug=None):
  category_page = None
  products = None
  if category_slug != None :
    category_page = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category_page , available=True)
  else:
    products = Product.objects.all().filter(available=True)
  return render(request, 'home.html' , {'category' : category_page , 'products' : products})


def productpage(request, category_slug , product_slug):
  try :
    product = Product.objects.get(category__slug=category_slug , slug=product_slug)
  except Exception as e :
    raise e
  return render(request, 'product.html', {'product' : product })

def cart_id (request) :
  #we create here (cart) if it's not exits !
  cart = request.session.session_key
  if not cart :
    cart = request.session.create()
  return cart

#we create here cart to Add Items
def add_cart(request , product_id) :
  product = product.objects.get(id = product_id)
  try :
    cart = Cart.objects.get(cart_id=cart_id(request))
  except Cart.DoesNotExist :
    cart =  Cart.objects.create(cart_id=cart_id(request))
    cart.save()
  try :
    cart_item = CartItem.objects.get(cart=cart , product=product)
    cart_item.quantity += 1
    cart_item.save()
  except  CartItem.DoesNotExist :
    cart_item = CartItem.objects.create(product=product , quantity = 1 , cart =cart)
    cart_item.save()

  return redirect('cart_details')

def cart_details (request, total= 0 , counter=0 , cart_items = None) :
  try :
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart , active=True)
    for cart_item in cart_items :
      total + (cart_item.product.price * cart_item.quantity)
      counter += cart_item.quantity
  except ObjectDoesNotExist :
    pass
  return render(request, 'cart.html' , dict(cart_items=cart_items , total=total , counter=counter))


