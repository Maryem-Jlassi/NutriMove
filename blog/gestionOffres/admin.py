from django.contrib import admin
from .models import offre
from Abonnements.models import Abonnements
# Register your models here.

class abonnerInLine(admin.StackedInline): #StackedInline est une classe fournie par Django admin qui permet d'afficher un modèle "en ligne"
    model=Abonnements #réservation doit être liée au modèle Reservation
    extra=1 
    #En mettant extra=1, tu obtiens une ligne vide supplémentaire pour ajouter une nouvelle réservation. 
    # #Si tu voulais plus de lignes vides pour ajouter des réservations, tu pourrais augmenter ce nombre.
    #readonly_fields=('abonnement_date',)
    can_delete=True



class priceFilter(admin.SimpleListFilter):
    title = "prix de l'offre" #Détermine le titre qui sera affiché dans l'interface d'administration pour ce filtre  # ba3d l BY 
    parameter_name = "offre_price"  #Définit le nom du paramètre qui sera utilisé dans l'URL lors du filtrage.

    def lookups(self, request, model_admin):
        return (
            ('low', 'moin de 50DT'),
            ('medium', 'Entre 50DT et 100Dt'),
            ('high', 'Plus que 100DT'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':  #Si l'utilisateur choisit "Past low", le queryset est filtré
                                    #pour retourner tous les offres dont le prix est < à 50 .
            return queryset.filter(price__lt=50)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=50,price__lte=100)
        elif self.value() == 'high':
            return queryset.filter(price__gt=100)
        return queryset

class offreAdmin(admin.ModelAdmin):
    # Affichage des offres
    list_display = ('category','titleOffre', 'program', 'start_date', 'end_date', 'price', 'coach_id', 'nutrisionist_id', 'capacity')  
    search_fields = ('titleOffre', 'start_date')  # Recherche par titre et date de début
    list_per_page = 2  # Pagination à 2 offres par page
    ordering = ('start_date',)  # Tri des offres par date de début
    list_filter = (priceFilter, 'titleOffre')  # Ajout du filtre de prix personnalisé
    inlines = [abonnerInLine] 
    # Organisation des champs dans l'interface admin
    fieldsets = (
        ('Description', {
            'fields': ('titleOffre', 'price', 'capacity', 'coach_id', 'nutrisionist_id','category',)
        }),
        ('Horaires', {
            'fields': ('start_date', 'end_date')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
    )

admin.site.register(offre, offreAdmin)  
