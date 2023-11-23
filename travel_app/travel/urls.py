from django.urls import path
from django.conf import settings
from django.conf.urls.static import static





from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.login_view, name="login"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register", views.register, name="register"),
    path('create_passenger', views.create_passenger, name='create_passenger'),
    path('list_passengers', views.list_passengers, name='list_passengers'),
    path('edit/<int:pk>', views.edit_passenger, name='edit_passenger'),
    path('delete/<int:pk>', views.delete_passenger, name='delete_passenger'),
    path('sales', views.create_sale, name='create_sale'),
    path('trips', views.create_trip, name='create_trip'),
    path('list_trips', views.list_trips, name='list_trips'),
    path('trip/edit/<int:pk>', views.edit_trip, name='edit_trip'),
    path('trip/delete/<int:pk>', views.delete_trip, name='delete_trip'),
    path('get_trip_price/<int:trip_id>/', views.get_trip_price, name='get_trip_price'),

] 


 