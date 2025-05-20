from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class BarbershopListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        barbershops = Barbershop.objects.all()
        serializer = BarbershopSerializer(barbershops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BarbershopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BarbershopDetailView(APIView):
    def get(self, request, pk):
        barbershop = get_object_or_404(Barbershop, pk=pk)
        serializer = BarbershopSerializer(barbershop)
        return Response(serializer.data)

    def put(self, request, pk):
        barbershop = get_object_or_404(Barbershop, pk=pk)
        serializer = BarbershopSerializer(barbershop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        barbershop = get_object_or_404(Barbershop, pk=pk)
        barbershop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceListCreateView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkPostListCreateView(APIView):
    def get(self, request):
        posts = WorkPost.objects.all()
        serializer = WorkPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(barber=request.user.barber_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListCreateView(APIView):
    def get(self, request):
        appointments = Appointment.objects.filter(customer=request.user)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
