from django.db import models
from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.IntegerField()
    projector = models.BooleanField(default=False)

    def get_reservations(self):
        return self.reservation_set.filter(date__gte=datetime.now().date()).order_by('date')

class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()


