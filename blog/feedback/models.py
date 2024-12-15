from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    choix_type=[ ('Service client', 'service client'),
                ('Produit','produit'),
                ('Expérience','expérience'),
                ('Suggestion','suggestion'),
                ('Autre','autre')
    ]
    feedback_type =models.CharField(max_length=20,choices =choix_type,default='Service client')
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)  
    anonymous = models.BooleanField(default=False)  
    date_created = models.DateTimeField(auto_now_add=True)
    #user = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True, blank=True)  
    comments = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    accept_terms = models.BooleanField(default=False)
    accept_moderation = models.BooleanField(default=False)


    def __str__(self):
        return f"Feedback {self.id} - {self.feedback_type}"


    '''def __str__(self):
        if self.user:
            return f"Feedback from {self.user.username}"
        else:
            return "Feedback from an anonymous user" 
    '''
    


    


