from colorfield.fields import ColorField
from django.db import models

# Create your models here.
class Text(models.Model):
    user =  models.CharField(max_length=200)
    speed = models.FloatField(default=1.0)
    color = models.CharField(max_length=6, default="FFFFFF")

class Book(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField()
    text = models.TextField()