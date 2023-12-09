from django.db import models

# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    type = models.ForeignKey('ProductType', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.code} - {self.name} - {self.price} - {self.type}'
    

class ProductType(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'