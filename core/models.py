

from django.db import models
from auths.models import Account
from datetime import timedelta
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    catgory_image=models.FileField(upload_to='category_image',blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image=models.FileField(upload_to='amenity/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
        ('Family', 'Family'),
        ('Delux', 'Deluxe'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    capacity= models.IntegerField(default=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='rooms')
    amenities = models.ManyToManyField(Amenity, related_name='rooms')
    hotel_images=models.FileField(upload_to='hotelroom/')
    is_booked=models.BooleanField(default=False)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'Room {self.room_number}'

    def book_room(self):
        """Mark the room as booked (i.e., unavailable)."""
        if self.is_available:
            self.is_available = False
            self.save()

    def checkout_room(self):
        """Mark the room as available after checkout."""
        if not self.is_available:
            self.is_available = True
            self.save()

    def update_price(self, new_price):
        """Update the price per night of the room."""
        self.price_per_night = new_price
        self.save()


class Booking(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE,related_name='booking')
    guest = models.ForeignKey(Account, on_delete=models.CASCADE) 
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_deadline = models.DateTimeField()
    payment_completed = models.BooleanField(default=False) 


   
    def __str__(self):
        return f'Booking for {self.guest_name} in Room {self.room.room_number}'




class Payment(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='')
    payment_status = models.CharField(max_length=20, default='Pending') 
    payment_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True) 
    user=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment of {self.amount} via {self.payment_method} - Status: {self.payment_status}'


class Photo(models.Model):
    hotel = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='photos')
    image = models.FileField(upload_to='hotel_photos/')
    created_at=models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return f"Photo of {self.hotel.room_number}"
    
    
    
    
class Review(models.Model):
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    review = models.TextField()
    user=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} on {self.hotel_room.room_number}"    