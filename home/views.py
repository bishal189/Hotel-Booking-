from django.shortcuts import render,redirect
from core.models import Category,HotelRoom,Booking,Payment
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json
from django.http import JsonResponse




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
        'home':True
    }
    return render(request,'home/home.html',context)


def all_rooms(request):
    hotel_room=HotelRoom.objects.all().order_by('-id')
    book=Booking.objects.all()
    rooms_with_status = []

    for room in hotel_room:
        is_booked = Booking.objects.filter(room=room).exists() 
        rooms_with_status.append({
            'room': room,
            'is_booked': is_booked
        })
      
    context={
        'hotel_room':hotel_room,
        'book':book,
        'rooms_with_status': rooms_with_status,
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
        room.is_booked=True
        room.save()
        
        
        # for time 
        
               
        checkin_date = timezone.make_aware(timezone.datetime.strptime(checkin_date, "%Y-%m-%d"))
        now = timezone.now()
        
        if checkin_date.date() == now.date():
          
            payment_deadline = now
        elif checkin_date.date() == now.date() + timedelta(days=1):
          
            payment_deadline = now + timedelta(hours=2)
        else:
            
            payment_deadline = now + timedelta(days=1)  


        booking=Booking.objects.create(
            guest_name=name,
            guest_email=email,
            guest_phone=phone_no,
            check_in_date=checkin_date,
            check_out_date=checkout_date,
            special_requests=message,
            room=room,
            guest=guest,
            payment_deadline=payment_deadline
        )
        
       
       
        # if booking.payment_deadline <= now:
        #     return redirect('payment', booking_id=booking.id)
        # elif booking.payment_deadline > now:
        #     return redirect('home')
        
      
        request.session['id'] = id
        request.session['booking_id']=booking.id
        messages.success(request, 'Booked  successfully!')
        return redirect('payment')

    
    
    else:
        room=HotelRoom.objects.get(id=id)
        context={
            'room':room,
            'id':id
        }
        return render(request,'home/book.html',context)
    
    
    



def dashboard(request):
    booking=Booking.objects.filter(guest=request.user,payment_completed=True)
    payments = Payment.objects.filter(booking__in=booking)  

    context={
        'book':booking,
        'payments':payments
    }
    return render(request,'home/dashboard.html',context)   




def delete_booking(request,id):
    booking=Booking.objects.get(id=id)
    booking.delete()
    messages.success(request,'booking has been deleted')
    return redirect('dashboard')
     
     
     
def payment(request):
    id = request.session.get('id')
    room=HotelRoom.objects.get(id=id)
    amount =room.price_per_night
    code = 'EUR'
    context={
        'room':room,
        'amount':amount,
        'code':code
    }
    

    return render(request,'home/payment.html',context)     


def payments(request):
    
    body=json.loads(request.body)
    booking=request.session.get('booking_id')
    book=Booking.objects.get(id=booking)
    
  
    payment=Payment.objects.create(
        user=request.user,
        transaction_id=body['transID'],
        payment_method=body['payment_method'],
        amount=body['amount'],
        payment_status=body['status'],
        booking=book



    )
    payment.save()
    
    book.payment_completed=True
    book.save()      
    data={
       
        'transID':payment.transaction_id

    }
    return JsonResponse(data)


   
def payment_complete(request):
    return render(request,'home/payment_complete.html')




def about_us(request):
    return render(request,'company/about.html')



def faqs(request):
    return render(request,'company/faq.html')


def terms(request):
    pass


def contact(request):
    return render(request,'company/contact.html')


def privacy(requset):
    return render(requset,'company/privacy.html')




def details(request):
    return render(request,'home/details.html')