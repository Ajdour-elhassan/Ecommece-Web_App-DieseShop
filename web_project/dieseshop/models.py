from django.db import models

#Create your models here.
class Product (models.Model) :
  name  = models.CharField(max_length= 15)
  price = models.IntegerField()
  about = models.TextField(max_length=60)

  def __str__(self):
    return 'user : ' + self.name