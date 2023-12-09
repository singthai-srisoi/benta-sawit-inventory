from django.db import models

# Create your models here.
class Vehicle(models.Model):
    reg_no = models.CharField(max_length=10)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.reg_no}'