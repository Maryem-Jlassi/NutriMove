from django.contrib import admin
from Abonnements.models import Abonnements
# Register your models here.


class abonnementAdmin(admin.ModelAdmin):
    #affichage des conferences
    list_display = ('offre', 'abonnement_date', 'confirmed', 'participant') 
    def make_confirmed(self, request, queryset):
        queryset.update(confirmed=True)
    make_confirmed.short_description = "Marquer comme confirmé"

    # Action pour déconfirmer la réservation
    def make_unconfirmed(self, request, queryset):
        queryset.update(confirmed=False)
    make_unconfirmed.short_description = "Marquer comme non confirmé"

    # Définir les actions disponibles
    actions = [make_confirmed, make_unconfirmed]



admin.site.register(Abonnements,abonnementAdmin)