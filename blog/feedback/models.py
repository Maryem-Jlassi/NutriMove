from django.db import models
#from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from produits.models import Produit
from users.models import CoachNutritionist


class Feedback(models.Model):
    feedback_item =models.ForeignKey(CoachNutritionist,on_delete=models.CASCADE,null=True,blank=True)
    feedback_produit=models.ForeignKey(Produit,on_delete=models.CASCADE,null=True,blank=True)
    TYPE_CHOICES = [
        ('très satisfait', 'Très satisfait'),
        ('satisfait', 'Satisfait'),
        ('neutre', 'Neutre'),
        ('insatisfait', 'Insatisfait'),
        ('très insatisfait', 'Très insatisfait')]
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),]
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)  
    anonymous = models.BooleanField(default=False)  
    date_created = models.DateTimeField(auto_now_add=True)
    satisfaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)



    
