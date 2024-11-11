from django.contrib import admin
from .models import Produit

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'categorie', 'prix', 'quantite_disponible', 'en_stock')
    search_fields = ('nom', 'reference')
    list_filter = ('categorie', 'en_stock')