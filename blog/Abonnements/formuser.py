from django import forms
from .models import Abonnements

class abonnementForm(forms.ModelForm):
    class Meta:
        model = Abonnements
        fields = [ 'offre','participant','abonnement_date', 'confirmed']  # Removed 'participant'