from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.IntegerField(default=15000)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_rentals')
    rental_date = models.DateField()
    return_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.username} - {self.car}"

class Invoice(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.IntegerField()
    issued_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice for {self.rental}"