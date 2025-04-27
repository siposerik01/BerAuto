from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    agent_dashboard_view,
    update_rental_view,
    admin_dashboard_view,
    save_car_view,
    update_user_view,
    save_invoice_view,
    rent_car
    )

urlpatterns = [
    path('', views.home, name='home'),
    #Login, Logout, Register
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    #UserProfil
    path('profil/', views.profile_view, name='profile'),

    #Agent Dashboard
    path('agent_dashboard/', agent_dashboard_view, name='agent_dashboard'),

    #Admin
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin_dashboard/save_car/', save_car_view, name='add_car'),
    path('admin_dashboard/save_car/<int:car_id>/', save_car_view, name='update_car'),
    path('admin_dashboard/update_user/<int:user_id>/', update_user_view, name='update_user'),

    #Invoice
    path('invoice/save/<int:rental_id>/', save_invoice_view, name='save_invoice'),         
    path('invoice/save/<int:rental_id>/<int:invoice_id>/', save_invoice_view, name='save_invoice'),

    #Rental Update
    path('rental/update/<int:rental_id>/', update_rental_view, name='update_rental'),

    #Rent Car
    path('rent/<int:car_id>/', views.rent_car, name='rent_car'),
]