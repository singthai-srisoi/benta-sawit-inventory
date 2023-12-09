from django.db import models

# Create your models here.
class Person(models.Model):
    PERSON_TYPE = [
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('driver', 'Driver'),
    ]
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    ic = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=PERSON_TYPE)
    
    # customer = Person(type='customer')
    def __str__(self):
        return f'{self.code} - {self.name} - {self.phone} - {self.type}'