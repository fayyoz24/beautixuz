from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


    
class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Barbershop(models.Model):
    """Model for barbershops"""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_barbershops')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='barbershop_logos/', blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='barbershops')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='barbershops')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    opening_hours = models.JSONField(default=dict)  # Store opening hours for each day
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name



class Service(models.Model):
    """Model for services that can be offered by barbershops and barbers"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Barber(models.Model):
    """Model for barbers"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='barber_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='barber_pictures/', blank=True, null=True)
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='barbers', null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='barbers', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='barbers', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    instagram_handle = models.CharField(max_length=100, blank=True)
    telegram_handle = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name


class BarbershopService(models.Model):
    """Model linking barbershops to services with pricing"""
    barbershop = models.ForeignKey(Barbershop, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='barbershop_services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('barbershop', 'service')
        
    def __str__(self):
        return f"{self.service.name} at {self.barbershop.name}"


class BarberService(models.Model):
    """Model linking barbers to services with custom pricing"""
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='barber_services')
    barbershop_service = models.ForeignKey(BarbershopService, on_delete=models.CASCADE, related_name='barber_services', null=True)
    custom_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                      help_text="Custom price for this barber, if different from standard barbershop price")
    custom_duration = models.IntegerField(null=True, blank=True,
                                        help_text="Custom duration in minutes, if different from standard barbershop duration")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('barber', 'service')
        
    def get_price(self):
        if self.custom_price is not None:
            return self.custom_price
        return self.barbershop_service.price if self.barbershop_service else None
    
    def get_duration(self):
        if self.custom_duration is not None:
            return self.custom_duration
        return self.barbershop_service.duration if self.barbershop_service else None
    
    def __str__(self):
        return f"{self.service.name} by {self.barber.user.get_full_name() or self.barber.user.username}"


class WorkPost(models.Model):
    """Model for barbers to showcase their work"""
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='work_posts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='work_posts/', null=True, blank=True)
    service = models.ManyToManyField(Service, related_name='work_posts')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} by {self.barber.first_name}"


class Like(models.Model):
    """Model for users liking barber's work posts"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(WorkPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


class AvailabilitySlot(models.Model):
    """Model for barber availability slots"""
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='availability_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.barber.first_name or self.barber.user.username} - {self.date} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    """Model for customer appointments with barbers"""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='appointments')
    barber_service = models.ForeignKey(BarberService, on_delete=models.CASCADE, related_name='appointments')
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.username} - {self.barber_service.service.name} with {self.barber.first_name or self.barber.user.username} on {self.date} at {self.start_time}"


class Review(models.Model):
    """Model for customer reviews of barbers"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.appointment}"
    