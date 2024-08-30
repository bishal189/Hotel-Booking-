from django.contrib import admin
from .models import *
# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display=['room_number','room_type','capacity','price_per_night']
admin.site.register(HotelRoom,HotelAdmin)



class categoryAdmin(admin.ModelAdmin):
    list_display=['name',]

admin.site.register(Category,categoryAdmin)


class AmenityAdmin(admin.ModelAdmin):
    list_display=['name',]
admin.site.register(Amenity,AmenityAdmin)


class bookingAdmin(admin.ModelAdmin):
    list_display=['guest_name','check_in_date','check_out_date','guest_email','guest_phone']
admin.site.register(Booking,bookingAdmin)



admin.site.register(Payment)
admin.site.register(Photo)
admin.site.register(Review)