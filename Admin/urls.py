
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='admin_index'),
    path('rooms/',views.Rooms,name='admin_category'),
    path('category/',views.cat,name='category_admin'),
    path('features/',views.features,name='features'),
    path('transactions/',views.trans,name='trans'),
    path('all/users/',views.all_users,name='all_users'),
    path('add/room/',views.add_room,name='add_room'),
    path('delete_room/<int:id>/',views.delete_room,name='delete_room'),
   
]