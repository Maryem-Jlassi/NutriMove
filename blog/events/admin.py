from django.contrib import admin
from .models import Event, Participant

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'date', 'image', 'location', 
        'organizer', 'max_participants', 'price', 'created_at', 
        'updated_at'
    )
    search_fields = ('title', 'description', 'organizer', 'location')
    list_filter = (
        'date',
        'organizer',  # Filtre par organisateur
        'max_participants',   # Filtre par capacité
        'price'       # Filtre par prix
    )
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20  # Nombre d'éléments par page

    fieldsets = (
        ('Informations de l\'événement', {
            'fields': ('title', 'description', 'date', 'location', 'organizer')
        }),
        ('Détails numériques', {
            'fields': ('max_participants', 'price','image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

admin.site.register(Event, EventAdmin)

class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'event', 'ticket_number', 
        'registration_date', 'payment_status'
    )
    search_fields = (
        'client__first_name', 'client__last_name', 
        'ticket_number', 'event__title'  # Recherche par titre de l'événement
    )
    list_filter = (
        'event', 
        'payment_status', 
        'registration_date',
        'client',  # Filtre par client
        'event__date'  # Filtre par date de l'événement
    )
    list_per_page = 20  # Nombre d'éléments par page

    fieldsets = (
        ('Informations sur le participant', {
            'fields': ('client', 'event', 'ticket_number', 'payment_status')
        }),
        ('Détails supplémentaires', {
            'fields': ('comments', 'seat_number')
        }),
        ('Détails de la réservation', {
            'fields': ('registration_date',),
        }),
    )

    readonly_fields = ('registration_date',)  # Marquer registration_date comme readonly

admin.site.register(Participant, ParticipantAdmin)
