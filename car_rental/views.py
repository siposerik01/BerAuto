from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Rental, Invoice, User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import date,datetime
from .models import Rental
from rest_framework.generics import ListCreateAPIView

User = get_user_model()

def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})

@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    

    Rental.objects.create(
        customer=request.user,
        car=car,
        request_rental_date=date.today(),
        is_approved=False,
        is_returned=False
    )
    messages.success(request, f'{car.brand} {car.model} sikeresen lefoglalva. Hamarosan felvesszük veled a kapcsolatot.')
    return redirect('home')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/'

class CustomLogoutView(LogoutView):
    next_page = '/'

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_customer = request.POST.get('is_customer') == 'on'
        is_agent = request.POST.get('is_agent') == 'on'
        is_admin = request.POST.get('is_admin') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ez a felhasználónév már foglalt.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_customer=is_customer,
            is_agent=is_agent,
            is_admin=is_admin
        )
        messages.success(request, 'Sikeres regisztráció! Jelentkezz be.')
        return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    rentals = user.rentals.select_related('car').all()
    context = {
        'user': user,
        'rentals': [
            {
                'car': str(rental.car),
                'request_rental_date': rental.request_rental_date,
                'start_date': rental.rental_date,
                'end_date': rental.return_date,
                'status': 'Visszavéve' if rental.is_returned else ('Jóváhagyva' if rental.is_approved else 'Függőben')
            }
            for rental in rentals
        ],
        'invoices': Invoice.objects.filter(rental__customer=user).select_related('rental', 'rental__car')
    }
    return render(request, 'profile.html', context)

@login_required
def agent_dashboard_view(request):
    user = request.user
    if not user.is_agent:
        return redirect('/')  

    rentals = Rental.objects.select_related('car', 'customer').all()
    invoices = Invoice.objects.select_related('rental', 'rental__car', 'rental__customer').all()

    return render(request, 'agent_dashboard.html', {
        'user': user,
        'rentals': rentals,
        'invoices': invoices,
    })

@require_POST
@login_required
def update_rental_view(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)

    if not (request.user.is_agent or request.user.is_admin):
        return redirect('/')

    rental_date_str = request.POST.get("rental_date")
    return_date_str = request.POST.get("return_date")
    rental.is_approved = request.POST.get("is_approved") == "True"
    rental.is_returned = request.POST.get("is_returned") == "True"
    rental.agent = request.user

    if rental_date_str:
        rental.rental_date = datetime.strptime(rental_date_str, "%Y-%m-%d").date()
    else:
        rental.rental_date = None

    if return_date_str:
        rental.return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
    else:
        rental.return_date = None

    rental.save()

    return redirect('admin_dashboard')

@require_POST
@login_required
def save_invoice_view(request, rental_id=None, invoice_id=None):
    if not (request.user.is_agent or request.user.is_admin):
        return redirect('/')

    if invoice_id:
        invoice = get_object_or_404(Invoice, id=invoice_id)
    else:
        rental = get_object_or_404(Rental, id=rental_id)
        if hasattr(rental, 'invoice'):
            messages.warning(request, "Ehhez a kölcsönzéshez már tartozik számla.")
            return redirect('admin_dashboard')

        napok = (rental.return_date - rental.rental_date).days or 1
        amount = rental.car.price * napok
        invoice = Invoice(rental=rental, amount=amount)

    try:
        invoice.amount = int(request.POST.get("amount", invoice.amount))
    except (ValueError, TypeError):
        pass

    invoice.paid = request.POST.get("paid") == "True"
    invoice.save()

    return redirect('admin_dashboard' if request.user.is_admin else 'agent_dashboard')

def admin_dashboard_view(request):
    if not request.user.is_admin:
        return redirect('/')

    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")
        user.address = request.POST.get("address")
        user.save()
        messages.success(request, "Sikeresen frissítetted az adataidat.")
        return redirect('admin_dashboard')

    rentals = Rental.objects.select_related('car', 'customer')

    for rental in rentals:
        if hasattr(rental, 'invoice'):
            rental.invoice = rental.invoice
        else:
            rental.invoice = None

    context = {
        'user': request.user,
        'cars': Car.objects.all(),
        'rentals': rentals,
        'users': User.objects.all()
    }
    return render(request, 'admin_dashboard.html', context)

@require_POST
@login_required
def save_car_view(request, car_id=None):
    if not request.user.is_admin:
        return redirect('/')

    car = get_object_or_404(Car, id=car_id) if car_id else Car()

    car.brand = request.POST.get("brand")
    car.model = request.POST.get("model")
    car.price = request.POST.get("price")
    car.mileage = request.POST.get("mileage")
    car.year = request.POST.get("year")
    car.available = request.POST.get("available") == "True"

    car.save()
    return redirect('admin_dashboard')

@require_POST
@login_required
def update_user_view(request, user_id):
    if not request.user.is_admin:
        return redirect('/')

    user = get_object_or_404(User, id=user_id)
    user.username = request.POST.get("username")
    user.email = request.POST.get("email")
    user.is_customer = "is_customer" in request.POST
    user.is_agent = "is_agent" in request.POST
    user.is_admin = "is_admin" in request.POST

    user.save()
    return redirect('admin_dashboard')