from django.urls import path
from .views import *

urlpatterns = [
    path('barbershops/', BarbershopListCreateView.as_view(), name='barbershop-list-create'),
    path('barbershops/<int:pk>/', BarbershopDetailView.as_view(), name='barbershop-detail'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('work-posts/', WorkPostListCreateView.as_view(), name='workpost-list-create'),

    path('barbers/create/', CreateBarberProfileView.as_view(), name='create-barber-profile'),

    path('all-work-posts/', AllWorkPostListCreateView.as_view(), name='all-posts'),
    path('all-work-posts/<int:pk>/', WorkPostDetailView.as_view(), name='all-posts/int'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
]
