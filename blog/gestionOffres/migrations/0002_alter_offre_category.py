# Generated by Django 5.1.3 on 2024-12-15 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionOffres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='category',
            field=models.CharField(blank=True, choices=[('kids', 'Kids'), ('teens', 'Teens'), ('other', 'Other')], max_length=50, null=True),
        ),
    ]
