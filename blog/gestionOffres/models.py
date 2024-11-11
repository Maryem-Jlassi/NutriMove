from django.db import models
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
# Create your models here.
class offre(models.Model):
 titleOffre=models.CharField(max_length=255)
 program = models.FileField(
        upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpeg', 'jpg'])],
        error_messages={'invalid_extension': 'Le fichier doit être au format PDF, PNG, JPEG ou JPG.'}  # Correction ici
    )
 capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=20,message="capacity must be under 20")])
 start_date=models.DateField()
 end_date=models.DateField()
 price=models.FloatField()
 coach_id=models.IntegerField()
 nutrisionist_id=models.IntegerField()
 def clean(self):
     if self.end_date <= self.start_date:
        raise ValidationError("End date must be after start date")
 def __str__(self):
    return f"title offre = {self.titleOffre}"
 class meta:
    verbose_name_plural="offres"