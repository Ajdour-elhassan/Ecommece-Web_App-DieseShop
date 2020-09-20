from .models import Category , Cart , CartItem
from .views import cart_id

# Counter_by_Display_count_IN_Card

def counter(request):
    item_count = 0
    if 'admin' in request.path :
        return {}
    else :
       try :
           cart = Cart.objects.filter(cart_id=cart_id(request))
           cart_items = CartItem.objects.all().filter(cart=cart[:1])
           for cart_item in cart_items :
              item_count += cart_item.quantity
       except Cart.DoesNotExist :
           item_count = 0
    return dict(item_count = item_count)

# menu_list_by_Categories

def menu_links(request) :
    links = Category.objects.all()
    return dict(links=links)



