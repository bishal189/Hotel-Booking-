

from django.db import models
from auths.models import Account
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    catgory_image=models.FileField(upload_to='category_image',blank=True,null=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
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
    hotel_images=models.FileField(upload_to='hotelroom')

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
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    guest = models.ForeignKey(Account, on_delete=models.CASCADE) 
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking for {self.guest_name} in Room {self.room.room_number}'
