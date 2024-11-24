# Generated by Django 5.1.3 on 2024-11-24 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestionOffres', '0001_initial'),
        ('users', '0005_passwordresettoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abonnements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('abonnement_date', models.DateTimeField()),
                ('offre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionOffres.offre')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client')),
            ],
            options={
                'verbose_name_plural': 'abonnements',
                'unique_together': {('offre', 'participant')},
            },
        ),
    ]
