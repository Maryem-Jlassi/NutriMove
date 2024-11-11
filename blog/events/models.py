from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import re
from users.models import Client

class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date = models.DateTimeField(verbose_name="Date")
    image = models.ImageField(upload_to='event_images/', verbose_name="Event Image")

    TUNISIAN_GOVERNORATES = [
        ('Ariana', 'Ariana'), ('Beja', 'Beja'), ('Ben Arous', 'Ben Arous'), 
        ('Bizerte', 'Bizerte'), ('Gabes', 'Gabes'), ('Gafsa', 'Gafsa'),
        ('Jendouba', 'Jendouba'), ('Kairouan', 'Kairouan'), ('Kasserine', 'Kasserine'), 
        ('Kebili', 'Kebili'), ('Manouba', 'Manouba'), ('Medenine', 'Medenine'), 
        ('Monastir', 'Monastir'), ('Nabeul', 'Nabeul'), ('Sfax', 'Sfax'), 
        ('Sidi Bouzid', 'Sidi Bouzid'), ('Siliana', 'Siliana'), ('Tataouine', 'Tataouine'), 
        ('Tozeur', 'Tozeur'), ('Tunis', 'Tunis'), ('Zaghouan', 'Zaghouan')
    ]
    location = models.CharField(max_length=255, choices=TUNISIAN_GOVERNORATES, verbose_name="Location")
    
    ORGANIZER_CHOICES = [
        ('nutritionist', 'Nutritionist'),
        ('coach', 'Coach'),
    ]
    organizer = models.CharField(max_length=100, choices=ORGANIZER_CHOICES, verbose_name="Organizer")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Price")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    
    max_participants = models.PositiveIntegerField(default=0, verbose_name="Max Participants")

    def __str__(self):
        return self.title

    def clean(self):
        if self.max_participants < 0:
            raise ValidationError('The maximum number of participants cannot be negative.')
        if self.price < 0:
            raise ValidationError('The price cannot be negative.')
        if len(self.title) < 5:
            raise ValidationError('The title must be at least 5 characters long.')
        if len(self.description) < 10:
            raise ValidationError('The description must be at least 10 characters long.')
        if self.location not in dict(self.TUNISIAN_GOVERNORATES):
            raise ValidationError(f"The location '{self.location}' is not a valid Tunisian governorate.")
        if self.date < timezone.now():
            raise ValidationError("The event date cannot be in the past.")
            
class Participant(models.Model):
    event = models.ForeignKey(Event, related_name='participants', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='participants', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    seat_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.client} - {self.event}"

    def clean(self):
        if not re.match(r'^[A-Z0-9]+$', self.ticket_number):
            raise ValidationError('The ticket number must contain only uppercase letters and digits.')
        if self.seat_number and len(self.seat_number) > 10:
            raise ValidationError('The seat number cannot exceed 10 characters.')
        if self.comments and len(self.comments) < 5:
            raise ValidationError('Comments must be at least 5 characters long.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean method before saving
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('client', 'event')
        ordering = ['-registration_date']  # Order participants by registration date
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
