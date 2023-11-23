from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Passenger, Trip, Sale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PassengerForm, TripForm, SaleForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse



@login_required
def index(request):
    return render(request, "travel/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("index")

        else:
            return render(request, "travel/login.html", {
                "message": "Nombre de usuario o contraseña inválida."
            })
    else:
        return render(request, "travel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel/register.html", {
                "message": "Las contraseñas no coinciden."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Nombre de usuario ya existe."
            })
        return HttpResponseRedirect(reverse("login"))

    else:
        return render(request, "travel/register.html")
    

@login_required
def list_passengers(request):
    # Obtener todos los pasajeros
    all_passengers = Passenger.objects.all()
   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_passengers = all_passengers.filter(
                Q(name__icontains=search_query) | Q(lastname__icontains=search_query) | Q(dni__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_passengers, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        passengers = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        passengers = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        passengers = paginator.page(paginator.num_pages)

    return render(request, 'travel/list_passengers.html', {'passengers': passengers, 'search_query': search_query})



@login_required
def delete_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    passenger.delete()
    messages.success(request, 'El pasajero se ha eliminado exitosamente.')
    return redirect('list_passengers')

@login_required
def edit_passenger(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)

    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del pasajero actualizada exitosamente.')
            return redirect('list_passengers')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = PassengerForm(instance=passenger)
    return render(request, 'travel/edit_passenger.html', {'form': form, 'passenger': passenger})


@login_required
def create_passenger(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Passenger.objects.filter(email=email).exists():
                messages.error(request, 'Ya existe un pasajero con este correo electrónico.')
            else:
                passenger = form.save(commit=False)
                passenger.user = request.user
                passenger.save()
                messages.success(request, 'Pasajero creado exitosamente.')
                return redirect('create_passenger')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = PassengerForm()
    return render(request, 'travel/create_passenger.html', {'form': form})


@login_required
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje creado exitosamente.')
            return redirect('create_trip')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TripForm()
    return render(request, 'travel/create_trip.html', {'form': form})

@login_required
def list_trips(request):
    # Obtener todos los pasajeros
    all_trips = Trip.objects.all()

   # Filtrar por nombre si se proporciona un término de búsqueda
    search_query = request.GET.get('search_query')
    if search_query:
        all_trips = all_trips.filter( Q(origin__icontains=search_query) | Q(destination__icontains=search_query))

    # Número de pasajeros por página
    items_per_page = 5
    paginator = Paginator(all_trips, items_per_page)

    # Obtener el número de página de la solicitud GET
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        trips = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        trips = paginator.page(paginator.num_pages)
    return render(request, 'travel/list_trips.html', {'trips': trips})

@login_required
def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    trip.delete()
    messages.success(request, 'El viaje se ha eliminado exitosamente.')
    return redirect('list_trips')



@login_required
def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del viaje actualizada exitosamente.')
            return redirect('list_trips')
        else:
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = TripForm(instance=trip)
    return render(request, 'travel/edit_trip.html', {'form': form, 'trip': trip})

@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        
        passenger_id = request.POST.get('passenger')
        trip_id = request.POST.get('trip')

        passenger = Passenger.objects.get(pk=passenger_id)
        trip = Trip.objects.get(pk=trip_id)

        form.fields['passenger'].initial = passenger
        form.fields['trip'].initial = trip

        if form.is_valid():
            form.save()
            messages.success(request, 'Venta creada exitosamente.')
            return redirect('create_sale')
        else:
            print("Errores de validación:")
            print(form.errors)
            messages.error(request, 'Corrija los errores en el formulario.')
    else:
        form = SaleForm()
    return render(request, 'travel/create_sale.html', {'form': form})



def get_trip_price(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)
        return JsonResponse({'price': trip.price_per_day})  # Devuelve el precio del viaje en formato JSON
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'El viaje no existe'}, status=404)