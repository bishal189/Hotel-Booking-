
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
    
    path('delete/features/<int:id>/',views.delete_features,name='delete_features'),
    path('edit/features/<int:id>/',views.edit_features,name='edit_feature'),
    path('add/features/',views.add_features,name='add_feature'),
    
    
    # for payment 
    path('delete/payment/<int:id>/',views.delete_payment,name='delete_payment'),
    
    
    # for toogle 
    
    path('toggle-room-status/',views.toggle_room_status,name='toggle_room'),
    path('book-room/',views.book_room,name='book_room'),
    
    
    # for photos
    path('hotel_photos/',views.hotel_photos,name='hotel_photos'),
    path('add_photos/',views.add_photos,name='add_photos'),
    path('delete_photos/<int:id>/',views.delete_photos,name='delete_photos'),
    path('edit_photos/<int:id>/',views.edit_photos,name='edit_photo'),

    
    
    # for contact
    path('all_contact/',views.all_contact,name='all_contact'),
    path('delete_contact/<int:id>/',views.delete_contact,name='delete_contact')

    
    
    

    
    
   
]