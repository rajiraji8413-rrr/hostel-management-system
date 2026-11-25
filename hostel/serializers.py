
from rest_framework import serializers
from .models import Student, Room, RoomAllocation, FeePayment


# STUDENT SERIALIZER
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

    def validate_email(self, value):
        queryset = Student.objects.filter(email=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A student with this email already exists."
            )

        return value


# ROOM SERIALIZER
class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, data):
        capacity = data.get(
            'capacity',
            self.instance.capacity if self.instance else None
        )

        available_beds = data.get(
            'available_beds',
            self.instance.available_beds if self.instance else None
        )

        if capacity is not None and available_beds is not None:

            if capacity <= 0:
                raise serializers.ValidationError(
                    {"capacity": "Room capacity must be greater than zero."}
                )

            if available_beds < 0:
                raise serializers.ValidationError(
                    {"available_beds": "Available beds cannot be negative."}
                )

            if available_beds > capacity:
                raise serializers.ValidationError(
                    {"available_beds": "Available beds cannot exceed room capacity."}
                )

        return data


# ROOM ALLOCATION SERIALIZER
class RoomAllocationSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source='student.student_name',
        read_only=True
    )

    room_number = serializers.CharField(
        source='room.room_number',
        read_only=True
    )

    class Meta:
        model = RoomAllocation
        fields = '__all__'

    def validate(self, data):

        student = data.get(
            'student',
            self.instance.student if self.instance else None
        )

        room = data.get(
            'room',
            self.instance.room if self.instance else None
        )

        if room and room.available_beds <= 0:
            raise serializers.ValidationError(
                {"room": "This room has no available beds."}
            )

        if student:
            existing = RoomAllocation.objects.filter(
                student=student,
                status='Active'
            )

            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError(
                    {"student": "This student already has an active room allocation."}
                )

        return data


# FEE PAYMENT SERIALIZER
class FeePaymentSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source='student.student_name',
        read_only=True
    )

    class Meta:
        model = FeePayment
        fields = '__all__'

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )

        return value
