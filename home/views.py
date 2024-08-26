from django.shortcuts import render
from core.models import Category,HotelRoom
# Create your views here.
from django.db.models import Count, Q
def home(request):
    category = Category.objects.annotate(
        available_rooms=Count('rooms', filter=Q(rooms__is_available=True))
    ) 
    
    hotel_room=HotelRoom.objects.all().order_by('-id')   
 
    context={
        'category':category,
        'hotel_room':hotel_room,
    }
    return render(request,'home/home.html',context)


def all_rooms(request):
    hotel_room=HotelRoom.objects.all().order_by('-id')  
    context={
        'hotel_room':hotel_room
    } 
    return render(request,'home/listing.html',context)