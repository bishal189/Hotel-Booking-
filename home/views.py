from django.shortcuts import render,redirect
from core.models import Category,HotelRoom,Booking,Payment,Photo,Amenity,Review
from home.models import BookMark,Contact
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator



def home(request):
    category = Category.objects.annotate(
        available_rooms=Count('rooms', filter=Q(rooms__is_available=True))
    ) 
    
    hotel_room=HotelRoom.objects.all().order_by('-id')
    reviews=Review.objects.all().order_by('-id')[:10]
    if request.user.is_authenticated:
            bookmarked_product_ids = BookMark.objects.filter(
                user=request.user
            ).values_list("product_id", flat=True)
    else:
        bookmarked_product_ids = []
        
        

    context={
        'category':category,
        'hotel_room':hotel_room,
        'home':True,
        'reviews':reviews,
        'book_mark':bookmarked_product_ids
    }
    return render(request,'home/home.html',context)



def all_rooms(request):
    hotel_room = HotelRoom.objects.all().order_by('-id')
    book = Booking.objects.all()
    features = Amenity.objects.all()  

    selected_features = request.GET.getlist('feature') 
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if selected_features:
        hotel_room = hotel_room.filter(amenities__name__in=selected_features).distinct()

    if min_price:
        hotel_room = hotel_room.filter(price_per_night__gte=min_price)
    if max_price:
        hotel_room = hotel_room.filter(price_per_night__lte=max_price)

    paginator = Paginator(hotel_room, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rooms_with_status = []
    for room in page_obj: 
        is_booked = Booking.objects.filter(room=room).exists()
        rooms_with_status.append({
            'room': room,
            'is_booked': is_booked
        })

    context = {
        'hotel_room': page_obj, 
        'book': book,
        'rooms_with_status': rooms_with_status,
        'features': features,  
        'page_obj':page_obj
    }
    return render(request, 'home/listing.html', context)



@login_required
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
    
    
    


@login_required
def dashboard(request):
    booking=Booking.objects.filter(guest=request.user,payment_completed=True)
    payments = Payment.objects.filter(booking__in=booking)  

    context={
        'book':booking,
        'payments':payments
    }
    return render(request,'home/dashboard.html',context)   



@login_required
def delete_booking(request,id):
    booking=Booking.objects.get(id=id)
    booking.delete()
    messages.success(request,'booking has been deleted')
    return redirect('dashboard')
     
     
@login_required    
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

@login_required
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


@login_required 
def payment_complete(request):
    return render(request,'home/payment_complete.html')




def about_us(request):
    return render(request,'company/about.html')



def faqs(request):
    return render(request,'company/faq.html')


def terms(request):
    pass


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if request.user:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                user=request.user,
            )
        else:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )

        return redirect('contact')

    return render(request, 'company/contact.html')



def privacy(requset):
    return render(requset,'company/privacy.html')




def details(request,id):
    room=HotelRoom.objects.get(id=id)
    photos=Photo.objects.filter(hotel=room)
    reviews=Review.objects.filter(hotel_room=room)
    photo=Photo.objects.filter(hotel=room)[:5]
    print(photos,'photos')
    context={
        'photos':photos,
        'room':room,
        'id':id,
        'reviews':reviews,
        'photo':photo
    }
    return render(request,'home/details.html',context)

@login_required
def review(request,id):
    if request.method=="POST":
        title=request.POST.get('title')
        name=request.POST.get('name')
        email=request.POST.get('email')
        review=request.POST.get('review')
        hotel_room=HotelRoom.objects.get(id=id)
        
        Review.objects.create(
            title=title,
            name=name,
            email=email,
            review=review,
            hotel_room=hotel_room,
            user=request.user
            
        )
        
        return redirect(reverse('details',kwargs={'id':id}))
   
   



@login_required(login_url="/account/login/")
@csrf_exempt
def toggle_bookmark(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("id")
            print(data,'============++++>')
            product = get_object_or_404(HotelRoom, id=product_id)
            bookmark, created = BookMark.objects.get_or_create(
                user=request.user,
                product=product
            )

            if not created:
                bookmark.delete()
                return JsonResponse({"success": True})

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)   
        
        
        

@login_required
def book_marks(request):
    book_mark=BookMark.objects.filter(user=request.user)
    book_mark_ids=BookMark.objects.filter(user=request.user).values_list("product_id", flat=True)
    context={
        'book_marks':book_mark,
        'book_mark_ids':book_mark_ids
    }
    return render(request,'home/book_mark.html',context)        


