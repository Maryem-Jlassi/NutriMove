from django import forms
from .models import comment
class commentForm(forms.ModelForm):
    class Meta:
        model=comment
        fields="__all__"
 