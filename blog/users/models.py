from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.db import models
import uuid
from django.utils import timezone
class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_nutritionist = models.BooleanField(default=False)


class Client(User): 
    sexe=models.CharField(max_length=50,null=False)  
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        null=False
    )
    weight = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(500.0)],
        null=False,
        help_text="Weight in kilograms"
    )
    height = models.FloatField(
        validators=[MinValueValidator(30.0), MaxValueValidator(300.0)],
        null=False,
        help_text="Height in centimeters"
    )
    goal_weight = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(500.0)],
        null=False,
        help_text="Desired weight in kilograms"
    )
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ('sedentary', 'Sedentary (little or no exercise)'),
            ('light', 'Lightly active (light exercise/sports 1-3 days/week)'),
            ('moderate', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
            ('active', 'Active (hard exercise/sports 6-7 days a week)'),
            ('very_active', 'Very active (very hard exercise/sports & a physical job)'),
        ],
        null=True,
        blank=True
    )
    profile_picture = models.TextField(
        default="https://e7.pngegg.com/pngimages/946/556/png-clipart-computer-icons-login-user-profile-client-smiley-%D0%B7%D0%BD%D0%B0%D1%87%D0%BA%D0%B8.png",
        validators=[URLValidator()],
        help_text="URL of the profile picture"
    )
    program_nutrition = models.FileField(upload_to='nutrition_programs/', null=True, blank=True)
    program_fitness = models.FileField(upload_to='fitness_programs/', null=True, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.username} - Client"
    
    
    
class CoachNutritionist(User):
    photo = models.TextField(
        default="https://www.shareicon.net/data/256x256/2016/07/21/799323_user_512x512.png",
        validators=[URLValidator()],
        help_text="URL of the profile photo"
    )
    certifications = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    client_id = models.ManyToManyField(Client)

    class Meta:
        verbose_name = "Coach/Nutritionist"
        verbose_name_plural = "Coaches/Nutritionists"
        
        
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

