
from django.db import models


class Student(models.Model):

    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    year_of_study = models.IntegerField()

    def __str__(self):
        return self.student_name


class Room(models.Model):

    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    available_beds = models.PositiveIntegerField()

    def __str__(self):
        return self.room_number


class RoomAllocation(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    allocation_date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default='Active'
    )

    def __str__(self):
        return f"{self.student.student_name} - {self.room.room_number}"


class FeePayment(models.Model):

    PAYMENT_STATUS = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(auto_now_add=True)

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    def __str__(self):
        return self.student.student_name
