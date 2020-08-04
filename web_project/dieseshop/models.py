from django.db import models

#Create your models here.
class Product (models.Model) :
  name  = models.CharField(max_length= 15)
  about = models.TextField(max_length=60)
  price = models.IntegerField()
  
  def __str__(self):
    return " Product's name  : " + self.name