from django import forms
from .models import Produit
from .models import Achat

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['client', 'produit']  # Fields to include in the form

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)  # Get the client from the view
        produit = kwargs.pop('produit', None)  # Get the produit from the view
        super().__init__(*args, **kwargs)
        if client:
            self.fields['client'].initial = client  # Set client
            self.fields['client'].widget.attrs['readonly'] = True  # Optionally make client field readonly
        if produit:
            self.fields['produit'].initial = produit  # Set produit
            self.fields['produit'].widget.attrs['readonly'] = True  


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = "__all__"