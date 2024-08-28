
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='admin_index'),
    path('rooms/',views.category,name='admin_category'),
    path('category/',views.cat,name='category_admin'),
    path('features/',views.features,name='features'),
    path('transitions/',views.trans,name='trans'),
   
]