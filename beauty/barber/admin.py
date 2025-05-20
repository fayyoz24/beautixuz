from django.contrib import admin
from .models import (
    Barbershop,
    Service,
    Barber,
    BarbershopService,
    BarberService,
    WorkPost,
    Like,
    AvailabilitySlot,
    Appointment
)
# Register your models here.
admin.site.register(Barbershop)
admin.site.register(Service)            
admin.site.register(Barber)
admin.site.register(BarbershopService)
admin.site.register(BarberService)
admin.site.register(WorkPost)
admin.site.register(Like)
admin.site.register(AvailabilitySlot)
admin.site.register(Appointment)