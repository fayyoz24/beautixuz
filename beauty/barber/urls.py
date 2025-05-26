from django.urls import path
from .views import *

urlpatterns = [
    path('barbershops/', BarbershopListCreateView.as_view(), name='barbershop-list-create'),
    path('barbershops/<int:pk>/', BarbershopDetailView.as_view(), name='barbershop-detail'),
    path('work-posts/', WorkPostListCreateView.as_view(), name='workpost-list-create'),

    path('barbers/create/', CreateBarberProfileView.as_view(), name='create-barber-profile'),
    path('barbers/<int:pk>/', BarberDetailView.as_view(), name='barber-detail'),
    path('all-work-posts/', AllWorkPostListCreateView.as_view(), name='all-posts'),
    # path('filter-all-work-posts/', WorkPostFilterByService.as_view(), name='filter-all-work-posts/'),
    path('all-work-posts/<int:pk>/', WorkPostDetailView.as_view(), name='all-posts/int'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('cities/', CityListView.as_view(), name='cities'),
    path('states/', ServiceListCreateView.as_view(), name='states'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]
