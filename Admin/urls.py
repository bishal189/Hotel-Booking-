
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
    path('edit_room/<int:id>/',views.edit_room,name='edit_room'),
    
    # for category 
    path("add/category/",views.add_category,name='add_category'),
    path("delete_category/<int:id>/",views.delete_category,name='delete_category'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    
    # for features 
    
    path('delete/features/<int:id>/',views.delete_features,name='delete_features')

    
    
   
]