from django.shortcuts import render,redirect
from auths.models import Account
from core.models import HotelRoom,Booking,Category,Amenity,Payment
from decimal import Decimal



# Create your views here.

def index(request):
    account=Account.objects.all().order_by('-id')[:5]
    rooms=HotelRoom.objects.all().order_by('-id')[:5]
    booking=Booking.objects.all().order_by('-id')[:5]
    account_count=account.count()
    context={
        'accounts':account,
        'account_count':account_count,
        'rooms':rooms,
        'booking':booking
    }
    
    return render(request,'Admin/index.html',context)


def Rooms(request):
    
    
    room=HotelRoom.objects.all().order_by('-id')
    context={
        'rooms':room
    }
    return render(request,'Admin/category.html',context)


def cat(request):
    category=Category.objects.all().order_by('-id')
    
    context={
        'category':category
            
    }
    return render(request,'Admin/cat.html',context)


def features(request):
    features=Amenity.objects.all().order_by('-id')
    
    
    context={
        'features':features
        
    }
    
    return render(request,'Admin/feature.html',context)




def trans(request):
    payment=Payment.objects.all().order_by('-id')
    context={
        'payments':payment
    }
    return render(request,'Admin/trans.html',context)



def all_users(request):
    users=Account.objects.all().order_by('-id')
    context={
        'users':users
    }
    return render(request,'Admin/user.html',context)





def add_room(request):
    if request.method=='POST':
        print(request.POST,'++++++++==dtat')
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





def delete_room(request,id):
    room=HotelRoom.objects.get(id=id)
    room.delete()
    return redirect('admin_category')