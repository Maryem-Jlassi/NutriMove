from django.db import models
from django.core.validators import RegexValidator
from gestionOffres.models import offre
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import Client
# Create your models here.


class Abonnements(models.Model):
    offre = models.ForeignKey(offre, on_delete=models.CASCADE) 
    participant = models.ForeignKey(Client, on_delete=models.CASCADE) 
    confirmed = models.BooleanField(default=False)
    abonnement_date = models.DateTimeField()

    def clean(self):
        if self.offre.end_date <= timezone.now().date():
            raise ValidationError("You can only participate in upcoming offers")

        
        # Check if the participant already has a subscription in the current month
        start_of_month = timezone.now().replace(day=1)
        if Abonnements.objects.filter(
            participant=self.participant,
            abonnement_date__gte=start_of_month
        ).exists():
            raise ValidationError("You can only have one subscription per month")

    class Meta:
        unique_together = ('offre', 'participant')
        verbose_name_plural = "abonnements"