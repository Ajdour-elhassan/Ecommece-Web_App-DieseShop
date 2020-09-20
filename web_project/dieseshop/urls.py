from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('' , views.home , name='home'),
   path('category/<slug:category_slug>' , views.home , name='products_by_category'),
   path('category/<slug:category_slug>/<slug:product_slug>', views.productpage, name="product_detail"),
   path('cart/add/<int:product_id>', views.add_cart , name='add_cart'),
   path("cart_details" , views.cart_details , name="cart_details"),
   path('cart/remove/<int:product_id>' , views.cart_remove , name='cart_remove'),
   path('cart/remove_cart_product/<int:product_id>' , views.remove_cart_product , name='remove_cart_product'),
   path('thankyou/<int:order_id>', views.thankyou_page , name='thankyou_page'),
   path('account/create/' , views.sign_up , name='signup'),
   path('account/signin/' , views.sign_in , name='signin'),
   path('account/signout/' , views.sign_out , name='signout'),
   path('Dashbord/'  , views.dashbord , name='dashbord'),
   path('search/' , views.search , name='search')

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)