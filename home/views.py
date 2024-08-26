from django.shortcuts import render,redirect
from core.models import Category,HotelRoom,Booking
from django.contrib import messages
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




def booking_forms(request,id):
    guest=request.user
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_no=request.POST.get('phone_no')
        message=request.POST.get('write_message')
        checkin_date=request.POST.get('checkin_date')
        checkout_date=request.POST.get('checkout_date')
        room=HotelRoom.objects.get(id=id)
        Booking.objects.create(
            guest_name=name,
            guest_email=email,
            guest_phone=phone_no,
            check_in_date=checkin_date,
            check_out_date=checkout_date,
            special_requests=message,
            room=room,
            guest=guest
        )
        
        messages.success(request, 'Booked  successfully!')
        return redirect('all_rooms')

    
    
    else:
        room=HotelRoom.objects.get(id=id)
        context={
            'room':room,
            'id':id
        }
        return render(request,'home/book.html',context)
    
    
    



def dashboard(request):
    return render(request,'home/dashboard.html')    