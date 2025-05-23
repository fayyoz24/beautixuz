from rest_framework import serializers
from .models import (
    Barbershop, Service, Barber, BarbershopService, BarberService,
    WorkPost, Like, AvailabilitySlot, Appointment, Review
)
from django.contrib.auth import get_user_model

User = get_user_model()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = '__all__'
        read_only_fields = ['user']


class BarbershopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbershop
        fields = '__all__'
        read_only_fields = ['owner']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class BarberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # or use UserSerializer for full details

    class Meta:
        model = Barber
        fields = '__all__'


class BarbershopServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarbershopService
        fields = '__all__'


class BarberServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberService
        fields = '__all__'


class WorkPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WorkPost
        fields = '__all__'
        read_only_fields = ['barber']

class AllWorkPostSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=True, read_only=True) 
    barber = BarberSerializer(read_only=True)
    
    class Meta:
        model = WorkPost
        fields = '__all__'
        read_only_fields = ['barber']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class AvailabilitySlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySlot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
