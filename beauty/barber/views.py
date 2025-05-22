from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, 
                                        IsAuthenticated,
                                )

from .permissions import (IsOwnerBarberOrReadOnly, IsSuperUserOrReadOnly,
                          IsBarberOwnerOrSuperuser)
from django.shortcuts import get_object_or_404

from .serializers import ServiceSerializer


class ServiceListCreateView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

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


class ServiceDetailView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Service, pk=pk)

    def get(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def put(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateBarberProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if user already has a Barber profile
        if hasattr(request.user, 'barber_profile'):
            return Response({"detail": "Barber profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BarberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BarberDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsBarberOwnerOrSuperuser()]
        return []  # No auth required for GET

    def get_object(self, pk):
        return get_object_or_404(Barber, pk=pk)

    def get(self, request, pk):
        barber = self.get_object(pk)
        serializer = BarberSerializer(barber)
        return Response(serializer.data)

    def put(self, request, pk):
        barber = self.get_object(pk)
        self.check_object_permissions(request, barber)
        serializer = BarberSerializer(barber, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        barber = self.get_object(pk)
        self.check_object_permissions(request, barber)
        serializer = BarberSerializer(barber, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        barber = self.get_object(pk)
        self.check_object_permissions(request, barber)
        barber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = WorkPost.objects.filter(barber=request.user.barber_profile)

        serializer = WorkPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            barber = request.user.barber_profile  # get the barber profile
        except Barber.DoesNotExist:
            return Response({"detail": "Only barbers can create posts."}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(barber=barber)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllWorkPostListCreateView(APIView):
    def get(self, request):
        posts = WorkPost.objects.all()

        serializer = AllWorkPostSerializer(posts, many=True)
        return Response(serializer.data)


class WorkPostDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerBarberOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(WorkPost, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = WorkPostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        serializer = WorkPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # barber remains unchanged
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 
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
