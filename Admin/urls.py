
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='admin_index'),
    path('category/',views.category,name='admin_category'),
   
]