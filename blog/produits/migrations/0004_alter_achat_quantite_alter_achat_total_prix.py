# Generated by Django 4.2 on 2024-11-24 14:33

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0003_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='quantite',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantité'),
        ),
        migrations.AlterField(
            model_name='achat',
            name='total_prix',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Prix total'),
        ),
    ]
