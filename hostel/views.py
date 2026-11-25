
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import (
    Student,
    Room,
    RoomAllocation,
    FeePayment
)

from .serializers import (
    StudentSerializer,
    RoomSerializer,
    RoomAllocationSerializer,
    FeePaymentSerializer
)


# STUDENT MANAGEMENT API
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ROOM MANAGEMENT API
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# ROOM ALLOCATION API
class RoomAllocationViewSet(viewsets.ModelViewSet):
    queryset = RoomAllocation.objects.select_related('student', 'room')
    serializer_class = RoomAllocationSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        room_id = serializer.validated_data['room'].pk
        room = Room.objects.select_for_update().get(pk=room_id)

        if room.available_beds <= 0:
            raise ValidationError({
                'room': 'No available beds in this room.'
            })

        allocation = serializer.save(room=room)

        if allocation.status == 'Active':
            room.available_beds -= 1
            room.save(update_fields=['available_beds'])

    @transaction.atomic
    def perform_update(self, serializer):
        old_allocation = self.get_object()
        old_room_id = old_allocation.room_id
        old_status = old_allocation.status

        new_room = serializer.validated_data.get(
            'room', old_allocation.room
        )
        new_room_id = new_room.pk
        new_status = serializer.validated_data.get(
            'status', old_status
        )

        room_ids = sorted({old_room_id, new_room_id})

        locked_rooms = Room.objects.select_for_update().filter(
            pk__in=room_ids
        ).order_by('pk')

        rooms = {room.pk: room for room in locked_rooms}

        old_room = rooms[old_room_id]
        selected_room = rooms[new_room_id]

        needs_new_bed = (
            new_status == 'Active'
            and (
                old_status != 'Active'
                or old_room_id != new_room_id
            )
        )

        if needs_new_bed and selected_room.available_beds <= 0:
            raise ValidationError({
                'room': 'No available beds in the selected room.'
            })

        serializer.save(room=selected_room)

        if old_status == 'Active' and (
            new_status != 'Active'
            or old_room_id != new_room_id
        ):
            old_room.available_beds = min(
                old_room.available_beds + 1,
                old_room.capacity
            )
            old_room.save(update_fields=['available_beds'])

        if needs_new_bed:
            selected_room.available_beds -= 1
            selected_room.save(update_fields=['available_beds'])

    @transaction.atomic
    def perform_destroy(self, instance):
        if instance.status == 'Active':
            room = Room.objects.select_for_update().get(
                pk=instance.room_id
            )

            room.available_beds = min(
                room.available_beds + 1,
                room.capacity
            )
            room.save(update_fields=['available_beds'])

        instance.delete()


# FEE PAYMENT API
class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.select_related('student')
    serializer_class = FeePaymentSerializer


# DASHBOARD API
class DashboardView(APIView):
    def get(self, request):
        total_students = Student.objects.count()
        total_rooms = Room.objects.count()

        total_allocations = RoomAllocation.objects.filter(
            status='Active'
        ).count()

        room_data = Room.objects.aggregate(
            total_capacity=Sum('capacity'),
            available_beds=Sum('available_beds')
        )

        total_capacity = room_data['total_capacity'] or 0
        available_beds = room_data['available_beds'] or 0
        occupied_beds = total_capacity - available_beds

        payment_data = FeePayment.objects.aggregate(
            total_payments=Count('id'),
            paid_amount=Sum(
                'amount',
                filter=Q(payment_status='Paid')
            ),
            pending_amount=Sum(
                'amount',
                filter=Q(payment_status='Pending')
            )
        )

        return Response({
            'total_students': total_students,
            'total_rooms': total_rooms,
            'total_allocations': total_allocations,
            'occupied_beds': occupied_beds,
            'available_beds': available_beds,
            'total_payments': payment_data['total_payments'],
            'paid_amount': payment_data['paid_amount'] or 0,
            'pending_amount': payment_data['pending_amount'] or 0
        })


# DASHBOARD FRONTEND
def dashboard_page(request):
    return render(request, 'hostel/dashboard.html')


# STUDENT MANAGEMENT FRONTEND
@ensure_csrf_cookie
def students_page(request):
    return render(request, 'hostel/students.html')


# ROOM MANAGEMENT FRONTEND
@ensure_csrf_cookie
def rooms_page(request):
    return render(request, 'hostel/rooms.html')


# ROOM ALLOCATION FRONTEND
@ensure_csrf_cookie
def allocations_page(request):
    return render(request, 'hostel/allocations.html')


# FEE PAYMENT FRONTEND
@ensure_csrf_cookie
def payments_page(request):
    return render(request, 'hostel/payments.html')
