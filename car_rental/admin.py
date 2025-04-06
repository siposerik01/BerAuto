from django.contrib import admin
from .models import User, Car, Rental, Invoice

# Register your models here.
#admin
#admin123
admin.site.register(User)
admin.site.register(Car)
admin.site.register(Rental)
admin.site.register(Invoice)