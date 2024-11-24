# Generated by Django 4.2 on 2024-11-24 01:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_client_sexe'),
        ('produits', '0002_alter_produit_note_moyenne_alter_produit_poids_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantité')),
                ('date_achat', models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date d'achat")),
                ('total_prix', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Prix total')),
                ('paiement_effectue', models.BooleanField(default=False, verbose_name='Paiement effectué')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achats', to='users.client', verbose_name='Client')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achats', to='produits.produit', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Achat',
                'verbose_name_plural': 'Achats',
            },
        ),
    ]
