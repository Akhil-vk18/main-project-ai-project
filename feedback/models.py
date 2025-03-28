from django.db import models
from booking.models import *
from user_app.models import *
# Create your models here.
class Feedback(models.Model):
    booking_id = models.OneToOneField(Book_Dr, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(blank=True,choices=[(i, i) for i in range(0, 6)], default=0)  # Ratings from 1 to 5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True)
