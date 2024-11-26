from django.db import models
from django.utils import timezone
from users.models import *

class Feedback(models.Model):

    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)  
    anonymous = models.BooleanField(default=False)  
    date_created = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        if self.user:
            return f"Feedback from {self.user.username}"
        else:
            return "Feedback from an anonymous user" 
    
    


    


