from django import forms
from .models import comment,reply
class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your comment here...'}),
        }


class replyForm(forms.ModelForm):
    class Meta:
        model = reply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your reply  here...'}),
        }