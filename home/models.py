from django.db import models
from auths.models import Account
from core.models import HotelRoom
# Create your models here.

class BookMark(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bookmark")
    product = models.ForeignKey(
        HotelRoom, on_delete=models.CASCADE, related_name="hotel_room"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.email} - {self.user.full_name} on {self.product.room_number}"
        )