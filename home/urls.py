
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home,name='home'),
    path('all-rooms/', views.all_rooms,name='all_rooms'),
    path('book-forms/<int:id>/', views.booking_forms,name='booking_forms'),
    path('dashboard/', views.dashboard,name='dashboard'),
]
