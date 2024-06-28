from django.db import models


class PersonManager(models.QuerySet):
    def as_dict(self):
        return [person.as_dict() for person in self]

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

    objects = PersonManager.as_manager()
    
    # customer = Person(type='customer')
    def __str__(self):
        return f'{self.code} - {self.name} - {self.phone} - {self.type}'
    
    def as_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'phone': self.phone,
            'ic': self.ic,
            'type': self.type,
        }