from django.contrib import admin
from .models import Produit
from .models import Achat

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'categorie', 'prix', 'quantite_disponible', 'en_stock')
    search_fields = ('nom', 'reference')
    list_filter = ('categorie', 'en_stock')

@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ('client', 'produit', 'quantite', 'total_prix', 'date_achat', 'paiement_effectue')
    search_fields = ('client__username', 'produit__nom')
    list_filter = ('date_achat', 'paiement_effectue')
