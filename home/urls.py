
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home,name='home'),
    path('all-rooms/', views.all_rooms,name='all_rooms'),
]
