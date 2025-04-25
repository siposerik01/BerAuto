from django.shortcuts import render
from .models import Car, Rental, Invoice, User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import (
    CarSerializer,
    RentalSerializer,
    InvoiceSerializer,
    UserRegistrationSerializer,
    MyTokenObtainPairSerializer
)
from .permissions import IsCustomer, IsAgent, IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_customer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

def home(request):
    return render(request, 'home.html')

class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]

class RentalListCreateView(ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [AllowAny]

class InvoiceListCreateView(ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CustomerRentalCreateView(CreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsCustomer]

class AgentRentalListView(ListAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAgent]

class AgentInvoiceCreateView(CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAgent]

class AdminCarListCreateView(ListAPIView, CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdmin]

class AdminCarDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdmin]