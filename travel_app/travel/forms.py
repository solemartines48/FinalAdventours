from django import forms
from .models import Passenger, Trip
from .models import Trip, Sale, TripStatus, TransportationType, SaleStatus, PaymentMethod

from django.core.exceptions import ValidationError

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['dni', 'name', 'lastname', 'age', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(PassengerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['name'].widget.attrs['placeholder'] = 'Ingrese el nombre'
        self.fields['name'].widget.attrs['required'] = True

        
        self.fields['lastname'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Ingrese el apellido'
        self.fields['lastname'].widget.attrs['required'] = True

        self.fields['age'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['age'].widget.attrs['placeholder'] = 'Ingrese la edad'
        self.fields['age'].widget.attrs['required'] = True

        self.fields['email'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese el correo electrónico'
        self.fields['email'].widget.attrs['required'] = True

        self.fields['phone_number'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingrese el número de teléfono'
        self.fields['phone_number'].widget.attrs['required'] = True
        self.fields['phone_number'].widget.attrs['type'] = 'tel'
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]+'

        self.fields['dni'].widget.attrs['class'] = 'form-control rounded-pill'
        self.fields['dni'].widget.attrs['placeholder'] = 'Ingrese el número de DNI'
        self.fields['dni'].widget.attrs['required'] = True

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['origin', 'destination', 'capacity', 'transportation_type', 'itinerary', 'trip_status', 'price_per_day']
        widgets = {
            'origin': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el origen'}),
            'destination': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el destino'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese la capacidad'}),
            'transportation_type': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in TransportationType]),
            'itinerary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el itinerario'}),
            'trip_status': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in TripStatus]),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Ingrese el precio por día'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['passenger', 'trip', 'arrival_date', 'departure_date', 'price', 'payment_method', 'installments', 'total_debt', 'sale_status']
        widgets = {
            'arrival_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control rounded-pill', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Precio', 'readonly': True}),
            'installments': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Número de cuotas'}),
            'total_debt': forms.NumberInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Deuda total', 'readonly': True}),
            'payment_method': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in PaymentMethod]),
            'sale_status': forms.Select(attrs={'class': 'form-control rounded-pill'}, choices=[(tag.name) for tag in SaleStatus]),
            'passenger': forms.Select(attrs={'class': 'form-control rounded-pill'}),
            'trip': forms.Select(attrs={'class': 'form-control rounded-pill'}),
        }

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['passenger'].queryset = Passenger.objects.all()  
        self.fields['trip'].queryset = Trip.objects.all() 
        self.fields['price'].widget.attrs['readonly'] = True
        if self.instance and hasattr(self.instance, 'trip') and self.instance.trip:
            print('si')
            self.fields['price'].initial = self.instance.trip.price_per_day
