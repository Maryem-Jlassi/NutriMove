
from django.db import models

class Produit(models.Model):
    CATEGORIES_CHOICES = [
        ('sport', 'Sport'),
        ('nutrition', 'Nutrition'),
    ]

    reference = models.CharField(max_length=50, primary_key=True, verbose_name="Référence produit")
    nom = models.CharField(max_length=100, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES_CHOICES,
        verbose_name="Catégorie"
    )
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    quantite_disponible = models.PositiveIntegerField(verbose_name="Quantité disponible")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    derniere_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    image = models.ImageField(upload_to='produits/', blank=True, null=True, verbose_name="Image")
    marque = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marque")
    poids = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Poids (kg)")
    dimensions = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dimensions")
    en_stock = models.BooleanField(default=True, verbose_name="En stock")
    note_moyenne = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name="Note moyenne")
    
    def __str__(self):
        return self.nom