from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StockDetails(models.Model):
  stock = models.CharField(max_length=255,unique=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
    unique_together = ("user","stock")
    
  
  
