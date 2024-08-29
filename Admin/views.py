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


def delete_category(request,id):
    category=Category.objects.get(id=id)   
    category.delete()
    return redirect('category_admin') 


    
def edit_category(request,id):
    if request.method=="POST":
        pass
    
    else:
        return render(request,"Admin/edit_category.html")    