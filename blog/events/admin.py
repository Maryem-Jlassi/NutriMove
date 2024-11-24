from django.contrib import admin
from .models import Event, Participant

# Admin configuration for the Event model
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'date', 'image', 'location',
        'organizer', 'max_participants', 'price', 'created_at',
        'updated_at', 'image'
    )
    search_fields = ('title', 'description', 'organizer', 'location')
    list_filter = (
        'date',
        'organizer',          # Filter by organizer
        'max_participants',   # Filter by max participants
        'price'               # Filter by price
    )
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20  # Number of items per page

    fieldsets = (
        ('Event Information', {
            'fields': ('image', 'title', 'description', 'date', 'location', 'organizer')
        }),
        ('Numeric Details', {
            'fields': ('max_participants', 'price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

admin.site.register(Event, EventAdmin)

# Admin configuration for the Participant model
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'event', 'client', 'ticket_number', 'registration_date', 'payment_status', 'fitness_level')
    
    search_fields = (
        'client__first_name', 'client__last_name',
        'ticket_number'  # Search by ticket number
    )
    list_filter = (
        'payment_status',
        'registration_date',
        'client',  # Filter by client
        'event'    # Filter by event
    )
    list_per_page = 20  # Number of items per page

    fieldsets = (
        ('Participant Information', {
            'fields': ('event', 'client', 'ticket_number', 'payment_status', 'fitness_level')
        }),
        ('Additional Details', {
            'fields': ('comments',)
        }),
        ('Reservation Details', {
            'fields': ('registration_date',)
        }),
    )

    readonly_fields = ('registration_date',)  # Mark registration_date as readonly

admin.site.register(Participant, ParticipantAdmin)
