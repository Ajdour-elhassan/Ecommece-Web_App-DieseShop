from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('' , views.home , name='home'),
   path('about' , views.about , name='about'),
   path('category/<slug:category_slug>' , views.home , name='products_by_category'),
   path('category/<slug:category_slug>/<slug:product_slug>', views.productpage, name="product_detail"),
   path("cart" , views.cart , name="cart"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)