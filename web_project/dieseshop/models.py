from django.db import models
from django.urls import reverse

# Create your models here.
class Category (models.Model):
  name = models.CharField(max_length=250, unique=True)
  slug = models.SlugField(max_length=250 , unique=True)
  image = models.ImageField(upload_to="./images")
  description = models.TextField(max_length=200 , blank=True , null=True)

  class Meta:
    ordering = ('name',)
    verbose_name = 'category'
    verbose_name_plural = 'categories'

# we gave here url/ or id as slug depends on ('products_by_category' = Url)
  def get_url(self):
    return reverse('products_by_category', args=[self.slug])

  def __str__(self):
    return self.name

class Product(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  name = models.CharField(max_length=20 , unique=True)
  slug = models.SlugField(max_length=250 , unique=True)
  description = models.TextField(max_length=200 , blank=True , null=True)
  price = models.DecimalField(max_digits=10 , decimal_places=2)
  image = models.ImageField(upload_to="./images")
  stock = models.IntegerField()
  available = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)


  class Meta:
    ordering = ('name',)
    verbose_name = 'product'
    verbose_name_plural = 'products'

  def get_url(self) :
    return reverse('product_detail' , args=[self.category.slug , self.slug])

  def __str__(self):
    return self.name

class Cart(models.Model) :
  cart_id = models.CharField(max_length=250 , blank=True , null=True)
  date_added = models.DateField(auto_now_add=True)
  class Meta:
    db_table = 'cart'
    ordering = ['date_added']

  def __str__(self):
    return  self.cart_id

class CartItem(models.Model) :
  product = models.ForeignKey(Product , on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
  quantity = models.IntegerField()
  available = models.BooleanField(default=True)

  class Meta :
    db_table = 'CartItem'
  
  def sub_total(self , x , y) :
      x = self.price
      y = self.quantity
      return x * y

  def __str__(self) :
    return self.product
  


