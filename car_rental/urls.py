from django.urls import path
from . import views
from .views import UserRegistrationView,CarListCreateView,RentalListCreateView, InvoiceListCreateView


urlpatterns = [
    path('', views.home, name='home'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('api/rentals/', RentalListCreateView.as_view(), name='rental-list-create'),
    path('api/invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),

    path('api/customer/rent/', views.CustomerRentalCreateView.as_view(), name='customer-rent'),
    path('api/agent/rentals/', views.AgentRentalListView.as_view(), name='agent-rentals'),
    path('api/agent/invoice/', views.AgentInvoiceCreateView.as_view(), name='agent-invoice'),
    path('api/admin/cars/', views.AdminCarListCreateView.as_view(), name='admin-cars'),
    path('api/admin/cars/<int:pk>/', views.AdminCarDetailView.as_view(), name='admin-car-detail'),
]