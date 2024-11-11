from django import forms
from .models import Feedback
from django.contrib.contenttypes.models import ContentType
from produits.models import Produit
from users.models import CoachNutritionist


class FeedbackForm(forms.ModelForm):
    accept_terms = forms.BooleanField(required=True, label="J'accepte les termes et conditions de ce formulaire.")
    accept_moderation = forms.BooleanField(required=True, label="En soumettant ce feedback, j'accepte que celui-ci soit modéré et publié sur le site sous réserve de validation.")

    FEEDBACK_CHOICES = [
        ('coach_nutritionist', 'Coach/Nutritionist'),
        ('produit', 'Produit')
    ]
    feedback_choice = forms.ChoiceField(
        choices=FEEDBACK_CHOICES,
        label="Sélectionnez ce que vous souhaitez évaluer",
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 

    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        label="Évaluation",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    satisfaction_choices = [
        ('', 'Sélectionnez'),
        ('très satisfait', '😀 Très satisfait'),
        ('satisfait', '😊 Satisfait'),
        ('neutre', '😐 Neutre'),
        ('insatisfait', '😞 Insatisfait'),
        ('très insatisfait', '😡 Très insatisfait'),
    ]
    
    satisfaction = forms.ChoiceField(choices=satisfaction_choices, required=True ,label="niveau de satisfaction",widget=forms.Select(attrs={'class': 'form-control'}))
    
    anonymous = forms.BooleanField(
        required=False,
        label="Soumettre de manière anonyme",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Feedback
        fields = ['feedback_choice','rating', 'satisfaction','anonymous', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

