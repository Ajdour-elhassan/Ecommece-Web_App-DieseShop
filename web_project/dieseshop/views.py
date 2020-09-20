from django.shortcuts import render , redirect , get_object_or_404
from . models import Category , Product , Cart , CartItem , Order , OrderItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required


# we create here category_page with sulg

def home (request , category_slug=None):
  category_page = None
  products = None
  if category_slug != None :
    category_page = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category_page , available=True)
  else:
    products = Product.objects.all().filter(available=True)
  return render(request, 'home.html' , {'category' : category_page , 'products' : products})

# we create here productpage with double_slugs

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
  product = Product.objects.get(id=product_id)
  try :
    cart = Cart.objects.get(cart_id=cart_id(request))
  except Cart.DoesNotExist :
    cart =  Cart.objects.create(cart_id=cart_id(request))
    cart.save()
  try :
    cart_item = CartItem.objects.get(cart=cart , product=product)
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1 # cart_item ++
    cart_item.save()
  except  CartItem.DoesNotExist :
    cart_item = CartItem.objects.create(product=product , quantity = 1 , cart =cart)
    cart_item.save()

  return redirect('cart_details')

# Cart_Detail_Adding And Item to ShoppingCard
def cart_details (request, total=0 , counter=0 , cart_items=None) :
  try :
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, available=True)
    for cart_item in cart_items :
      #displaying items on Add to cart page()
      # started with 0 + (price * quantity)
      total += (cart_item.product.price * cart_item.quantity)
      counter += cart_item.quantity # quantity = quantity - 1
  except ObjectDoesNotExist :
    pass # if not item added to cart just pass(Ignorate it )

  #payment process:
  stripe.api_key = settings.STRIPE_SECRET_KEY
  stripe_total = int(total * 100)
  description = 'Z-Stor-New order'
  data_key = settings.STRIPE_PUBLISHABLE_KEY
  if request.method == "POST" :
    try:
      token = request.POST['stripeToken']
      email = request.POST['stripeEmail']
      billingName = request.POST['stripeBillingName']
      billingAddress1 = request.POST['stripeBillingAddressLine1']
      billingCity = request.POST['stripeBillingAddressCity']
      billingPostcode = request.POST['stripeBillingAddressZip']
      billingCountry = request.POST['stripeBillingAddressCountryCode']
      shippingName = request.POST['stripeShippingName']
      shippingAddress1 = request.POST['stripeShippingAddressLine1']
      shippingCity = request.POST['stripeShippingAddressCity']
      shippingPostcode = request.POST['stripeShippingAddressZip']
      shippingCountry = request.POST['stripeShippingAddressCountryCode']

      customer = stripe.Customer.create(
        email = email ,
        source = token
      )
      #Create oder_View
      try :
        order_details = Order.objects.create(
          token = token,
          total = total,
          emailAddress = email,
          billingName = billingName,
          billingAddress1 = billingAddress1,
          billingCity = billingCity,
          billingPostcode = billingPostcode,
          billingCountry = billingCountry,
          shippingName=shippingName,
          shippingAddress1 = shippingAddress1,
          shippingCity = shippingCity,
          shippingPostcode = shippingPostcode,
          shippingCountry = shippingCountry
        )
        order_details.save()
        for order_item in cart_items :
            or_item = OrderItem.objects.create(
              product = order_item.product.name,
              quantity = order_item.quantity,
              price = order_item.product.price,
              order = order_details,
            )
            or_item.save()

            #reducing_stock
            products = Product.objects.get(id=order_item.product.id)
            products.stock =int(order_item.product.stock - order_item.quantity)
            products.save()
            order_item.delete()

            print('order has been successfully Done')
            return redirect('thankyou_page' , order_details.id)

      except ObjectDoesNotExist:
        pass # Pass and Ignore it !

        # making_charge_payment!
      charge = stripe.Charge.create(
            amount = stripe_total,
            currency = 'usd',
            description = description,
            customer = customer.id
      )
    except stripe.error.CardError as e :
      return False, e
      
  return render(request, 'cart.html' , dict(cart_items=cart_items , total=total , counter=counter , strip_total=stripe_total , data_key=data_key , description=description ))

# CreateView_Delete Every Single Item on ShoppingCard
def cart_remove (request , product_id) :
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product , cart=cart)
    if cart_item.quantity > 1 :
       cart_item.quantity -= 1 # quantity = quantity - 1
       cart_item.save()
    else :
      cart_item.delete()
    return redirect('cart_details')

 # CreateView_Delete All Item on ShoppingCard
def remove_cart_product (request , product_id) :
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product , id=product_id)
    cart_item = CartItem.objects.get(product=product , cart=cart)
    cart_item.delete()
    return redirect ('cart_details')

# ThankYouPage!

def thankyou_page(request , order_id):
    if order_id :
      customer_order = get_object_or_404(Order , id=order_id)
    return render(request , 'thankyoupage.html' , { 'customer_order' : customer_order })


#SignInView

def sign_up(request) :
  if request.method == "POST" :
     form = SignUpForm(request.POST)
     if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        signUp_user = User.objects.get(username=username)
        customer_group = Group.objects.get(name='Customer')
        customer_group.user_set.add(signUp_user)
        redirect('signin')
  else :
    form = SignUpForm()
  return render(request, 'signUp.html' , {'form' : form})

# SignInFormView

def sign_in(request) :
  if request.method == "POST" :
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username , password=password)
      if user is not None :
        login(request, user)
        return redirect('home')
      else :
          redirect('signup')
  else :
    form = AuthenticationForm()

  return render(request, 'singIn.html' , {'form' : form})

# SingOutView

def sign_out(request):
  logout(request)
  return redirect('home')



# BuildOrderHistoryPage

@login_required(redirect_field_name='next', login_url='signin')
def dashbord(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        order_details = Order.objects.filter(emailAddress=email)
        print(email)
        print(order_details)
    return render(request, 'dashbord.html', {'order_details': order_details})


# SearchViewFunction

def search(request) :
  products = Product.objects.filter(name__contains=request.GET['title'])
  return render(request, 'home.html' , {'products' : products})
  