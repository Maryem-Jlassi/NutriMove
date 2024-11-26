from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    accept_terms = forms.BooleanField(required=True, label="J'accepte les termes et conditions de ce formulaire.")
    accept_moderation = forms.BooleanField(required=True, label="En soumettant ce feedback, j'accepte que celui-ci soit modéré et publié sur le site sous réserve de validation.")
    
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Évaluation",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    anonymous = forms.BooleanField(
        required=False,
        label="Soumettre de manière anonyme",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Feedback
        fields = ['rating','anonymous', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
