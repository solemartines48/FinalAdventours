from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from enum import Enum

class User(AbstractUser):
    pass

class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    passenger_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dni = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.lastname} - DNI: {self.dni}"
    


class TripStatus(Enum):
    ACTIVE = 'Activo'
    CANCELLED = 'Cancelado'
    COMPLETED = 'Completado'



class TransportationType(Enum):
    BUS = 'Bus'
    TRAIN = 'Tren'
    PLANE = 'Avión'
    CAR = 'Carro'    

class Trip(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    capacity = models.IntegerField()
    TRANSPORT_CHOICES = [
        (tag.name, tag.value) for tag in TransportationType
    ]
    transportation_type = models.CharField(max_length=50, choices=TRANSPORT_CHOICES)
    itinerary = models.TextField(blank=True, null=True)
    trip_status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in TripStatus], default=TripStatus.ACTIVE.value)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Viaje desde {self.origin} hacia {self.destination}"


class SaleStatus(Enum):
    PENDING = 'Pendiente'
    IN_PROGRESS = 'En Proceso'
    CANCELLED = 'Cancelado'
    COMPLETED = 'Terminado'


class PaymentMethod(Enum):
    CASH = 'Efectivo'
    CARD = 'Tarjeta'
    PAYPAL = 'PayPal'

class Sale(models.Model):
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in PaymentMethod])
    installments = models.IntegerField(default=1) 
    total_debt = models.DecimalField(max_digits=10, decimal_places=2)
    sale_status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in SaleStatus], default=SaleStatus.PENDING.value)
    def __str__(self):
        return f"Sale by {self.passenger} for {self.trip} on {self.sale_date}"