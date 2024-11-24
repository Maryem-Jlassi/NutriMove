from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from users.models import Client
from decimal import Decimal








class Produit(models.Model):
    CATEGORIES_CHOICES = [
        ('sport', 'Sport'),
        ('nutrition', 'Nutrition'),
    ]

    reference = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name="Référence produit",
        validators=[RegexValidator(regex='^[A-Za-z0-9-]+$', message="La référence doit contenir uniquement des lettres, chiffres et tirets.")]
    )
    nom = models.CharField(max_length=100, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES_CHOICES,
        verbose_name="Catégorie"
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix",
        validators=[MinValueValidator(0.01)]
    )
    quantite_disponible = models.PositiveIntegerField(
        verbose_name="Quantité disponible",
        validators=[MinValueValidator(0)]
    )
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    derniere_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    image = models.ImageField(upload_to='produits/', blank=True, null=True, verbose_name="Image")
    marque = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marque")
    poids = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Poids (kg)",
        validators=[MinValueValidator(0.01)]
    )
    dimensions = models.CharField(max_length=50, blank=True, null=True, verbose_name="Dimensions")
    en_stock = models.BooleanField(default=True, verbose_name="En stock")
    note_moyenne = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Note moyenne",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return self.nom



class Achat(models.Model):
    client = models.ForeignKey(
        'users.Client', 
        on_delete=models.CASCADE,
        related_name='achats',
        verbose_name="Client"
    )
    produit = models.ForeignKey(
        'Produit', 
        on_delete=models.CASCADE,
        related_name='achats',
        verbose_name="Produit"
    )
    quantite = models.PositiveIntegerField(
    verbose_name="Quantité",
    validators=[MinValueValidator(1)],
    default=1  # Default value set to 1
)

    date_achat = models.DateTimeField(default=timezone.now, verbose_name="Date d'achat")
    total_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix total",
        validators=[MinValueValidator(0.01)],
        default=Decimal('0.00')
    )
    paiement_effectue = models.BooleanField(default=False, verbose_name="Paiement effectué")
    
  

    def __str__(self):
        return f"{self.client.username} a acheté {self.produit.nom} - {self.quantite} unité(s)"

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"