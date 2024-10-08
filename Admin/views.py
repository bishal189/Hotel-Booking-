from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from auths.models import Account
from core.models import HotelRoom,Booking,Category,Amenity,Payment,Photo
from home.models import Contact
from decimal import Decimal
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superadmin


# Create your views here.
@user_passes_test(is_superuser)
def index(request):
    account=Account.objects.all().order_by('-id')[:5]
    rooms=HotelRoom.objects.all().order_by('-id')[:5]
    booking=Booking.objects.all().order_by('-id')[:5]
    booked=HotelRoom.objects.filter(is_booked=True).order_by('-id').count()
    account_count=account.count()
    total_room=rooms.count()
    payment=Payment.objects.all().order_by('-id')
    total=0
    for payment in payment:
        total=payment.amount + total
        
    context={
        'accounts':account,
        'account_count':account_count,
        'rooms':rooms,
        'booking':booking,
        'booked':booked,
        'total_room':total_room,
        'total':total
    }
    
    return render(request,'Admin/index.html',context)

@user_passes_test(is_superuser)
def Rooms(request):
    
    
    room=HotelRoom.objects.all().order_by('-id')
    context={
        'rooms':room
    }
    return render(request,'Admin/category.html',context)

@user_passes_test(is_superuser)
def cat(request):
    category=Category.objects.all().order_by('-id')
    
    context={
        'category':category
            
    }
    return render(request,'Admin/cat.html',context)

@user_passes_test(is_superuser)
def features(request):
    features=Amenity.objects.all().order_by('-id')
    
    
    context={
        'features':features
        
    }
    
    return render(request,'Admin/feature.html',context)



@user_passes_test(is_superuser)
def trans(request):
    payment=Payment.objects.all().order_by('-id')
    context={
        'payments':payment
    }
    return render(request,'Admin/trans.html',context)


@user_passes_test(is_superuser)
def all_users(request):
    users=Account.objects.all().order_by('-id')
    context={
        'users':users
    }
    return render(request,'Admin/user.html',context)




@user_passes_test(is_superuser)
def add_room(request):
    if request.method=='POST':
        room_number = request.POST.get('room_number','')
        room_type = request.POST.get('room_type','')
        capacity = request.POST.get('capacity','')
        features = request.POST.getlist('features','')
        
        category = request.POST.get('category','')
        category=Category.objects.get(id=category)
        description = request.POST.get('description','')
        radio = request.POST.get('radio')
        is_available = True if radio == 'on' else False
        price_per_night=request.POST.get('price_per_night')
        photos = request.FILES.get('photos')
        print(photos,'photos')
        if price_per_night:
            price_per_night = Decimal(price_per_night)

        
        room=HotelRoom.objects.create(
            room_number=room_number,
            room_type=room_type,
            capacity=capacity,
            category=category,
            description=description,
            is_available=is_available,
            price_per_night=price_per_night,
            hotel_images=photos,
            
        )
        room.amenities.add(*features)
        room.save()
        print('item has been saved')
        
        
    features=Amenity.objects.all().order_by("-id")
    category=Category.objects.all().order_by("-id")
    context={
        'features':features,
        'category':category
    }
    return render(request,'Admin/add_room.html',context)




@user_passes_test(is_superuser)
def delete_room(request,id):
    room=HotelRoom.objects.get(id=id)
    room.delete()
    return redirect('admin_category')

@user_passes_test(is_superuser)
def edit_room(request,id):
    room=HotelRoom.objects.get(id=id)
    if request.method=="POST":
        print('request data',request.POST)
        room_number = request.POST.get('room_number','')
        room_type = request.POST.get('room_type','')
        capacity = request.POST.get('capacity','')
        features = request.POST.getlist('features','')
        
        category = request.POST.get('category','')
        category=Category.objects.get(id=category)
        description = request.POST.get('description','')
        radio = request.POST.get('is_featured')
       
        price_per_night=request.POST.get('price_per_night')
        photos = request.FILES.get('photos')
        if photos:
           room.hotel_images=photos
            
       
      
                
        if price_per_night:
            price_per_night = Decimal(price_per_night)
        
        room.room_number=room_number
        room.room_type=room_type
        room.capacity=capacity
        room.category=category
        room.description=description
        room.is_available=radio
        room.price_per_night=price_per_night     
        room.amenities.add(*features)
        room.save()
        return redirect('admin_category')
    
    else:
        selected_feature_ids = room.amenities.values_list('id', flat=True)
        category=Category.objects.all().order_by('-id')
        selected_category_id = room.category.id 
        features=Amenity.objects.all().order_by('-id')
        
        print(room.hotel_images)

        context={
            'room':room,
            'id':id,
            'edit':True,
            'selected_feature_ids':selected_feature_ids,
            'selected_category_id': selected_category_id,
            'category':category,
            'features':features
        }
        return render(request,'Admin/edit_room.html',context)
    
    
    
    
    
# for category 
@user_passes_test(is_superuser)
def add_category(request):
    if request.method == "POST":
        category_name=request.POST.get('category_name')
        photos = request.FILES.get('photos')
        print(request.POST,'++++++++++++++>S')
        
        Category.objects.create(
            name=category_name,
            catgory_image=photos
        )
        print('saved')
        return redirect('category_admin')
    else:
        return render(request,'Admin/add_category.html')

@user_passes_test(is_superuser)
def delete_category(request,id):
    category=Category.objects.get(id=id)   
    category.delete()
    return redirect('category_admin') 


@user_passes_test(is_superuser)
def edit_category(request,id):
    category=Category.objects.get(id=id)
    if request.method=="POST":
        category_name=request.POST.get('category_name')
        photos = request.FILES.get('photos')
        category.name=category_name
        if photos:
            category.catgory_image=photos
            
        category.save()
        return redirect('category_admin')
        
      
        
    
    else:
        context={
            'id':id,
            'category':category,
            'edit':True
        }
        return render(request,"Admin/edit_category.html",context)    
    
    
    
    
# for fatures 

@user_passes_test(is_superuser)
def delete_features(request,id):
    try:
        feature=Amenity.objects.get(id=id)
        feature.delete()
        return redirect('features')
    
    except:
        pass

@user_passes_test(is_superuser)
def edit_features(request,id):
    feature=Amenity.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get('feature_name')
        photos=request.FILES.get('photos')
        
        if photos:
            feature.image=photos
        feature.name=name
        feature.save()
        print('saved')
        return redirect('features')    
    
    else:
        context={
            'id':id,
            'feature':feature,
            'edit':True
        }
        return render(request,'Admin/edit_feature.html',context)            
 
@user_passes_test(is_superuser)    
def add_features(request):
    if request.method=='POST':
        name=request.POST.get('feature_name')
        photos=request.FILES.get('photos')
        Amenity.objects.create(
            name=name,
            image=photos
        )
        print('saved features')
        return redirect('features')
   
    else:
        return render(request,'Admin/add_feature.html')    
    
    
    
# for transition 

@user_passes_test(is_superuser)
def delete_payment(request,id):
    try:
        payment=Payment.objects.get(id=id)
        payment.delete()
        return redirect('trans')
    
    except:
        pass
            
            


# for toggle booking and is available 
@user_passes_test(is_superuser)
@require_POST
def toggle_room_status(request):
    room_id = request.POST.get('room_id')
    status_type = request.POST.get('status_type') 
    new_status = request.POST.get('new_status') == 'true'  

    try:
        room = HotelRoom.objects.get(id=room_id)
        if status_type == 'is_booked':
            room.is_booked = new_status
        elif status_type == 'is_available':
            room.is_available = new_status
        room.save()
        print('saved')
        return JsonResponse({'success': True})
    except HotelRoom.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'}, status=404)            
    
    
@user_passes_test(is_superuser)   
def book_room(request):
    rooms =Booking.objects.all().order_by('-id')      
    context={
        'rooms':rooms
    }
    return render(request,'Admin/book_room.html',context)    


@user_passes_test(is_superuser)
def hotel_photos(request):
    photos=Photo.objects.all().order_by('-id')
    context={
        'photos':photos
    }
    return render(request,'Admin/photos.html',context)    

@user_passes_test(is_superuser)
def add_photos(request):
    if request.method=="POST":
        room_id=request.POST.get('room')
        hotel_room=HotelRoom.objects.get(id=room_id)
        photos=request.FILES.get('photos')
        
        Photo.objects.create(
            hotel=hotel_room,
            image=photos,
        )
        print('saved')
        return redirect('hotel_photos')
    hotel=HotelRoom.objects.all().order_by('-id')
    context={
        'hotels':hotel
    }
    return render(request,'Admin/add_photos.html',context)    

@user_passes_test(is_superuser)
def edit_photos(request, id):
    photo = Photo.objects.get(id=id)
    
    if request.method == "POST":
        room_id = request.POST.get('room')
        hotel_room = HotelRoom.objects.get(id=room_id)
        
        # Get the current image if no new image is uploaded
        current_image = request.FILES.get('current_image')
        
       
        
        # Get the new image if uploaded
        new_photo = request.FILES.get('photos')
        photo.hotel = hotel_room
        
        if new_photo:
            photo.image = new_photo
        else:
            if current_image:
                photo.image = current_image
        
        photo.save()
        print('saved')
        return redirect('hotel_photos')
    else:
        hotel = HotelRoom.objects.all().order_by('-id')
        
        context = {
            'photo': photo,
            'hotels': hotel,
            'id': id,
            'edit': True
        }
        return render(request, 'Admin/edit_photo.html', context)

@user_passes_test(is_superuser)
def delete_photos(request,id):
    try:
        photo=Photo.objects.get(id=id)
        photo.delete()
        return redirect('hotel_photos')
    
    
    except:
        pass
        
@user_passes_test(is_superuser)        
def all_contact(request):
    contact=Contact.objects.all().order_by('-id')
    context={
        'contacts':contact
    }        
    
    return render(request,'Admin/contact.html',context)



@user_passes_test(is_superuser)
def delete_contact(request,id):
    try:
        contact=Contact.objects.get(id=id)
        contact.delete()
        return redirect('all_contact')
    
    
    except:
        pass
    