from django.shortcuts import render
from auths.models import Account
from core.models import HotelRoom,Booking


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
    return render(request,'Admin/category.html')