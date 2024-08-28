from django.shortcuts import render
from auths.models import Account
from core.models import HotelRoom,Booking,Category,Amenity,Payment


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


def category(request):
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