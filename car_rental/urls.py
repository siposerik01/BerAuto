from django.urls import path
from . import views
from .views import UserRegistrationView,CarListCreateView,RentalListCreateView, InvoiceListCreateView

urlpatterns = [
    path('', views.home, name='home'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('api/rentals/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('api/invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
]