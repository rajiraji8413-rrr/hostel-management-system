
from django.contrib import admin
from .models import Student, Room, RoomAllocation, FeePayment

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(RoomAllocation)
admin.site.register(FeePayment)
