
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.home,name='home'),
    path('all-rooms/', views.all_rooms,name='all_rooms'),
    path('book-forms/<int:id>/', views.booking_forms,name='booking_forms'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('delete/booking/<int:id>/', views.delete_booking,name='delete_booking'),
    path('payment/', views.payment,name='payment'),
    path('payments/',views.payments,name='payments'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('about_us/', views.about_us, name='about_us'),
    path('faqs/', views.faqs, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
]
