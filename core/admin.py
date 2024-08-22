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