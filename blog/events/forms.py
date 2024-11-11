from django import forms
from .models import Participant
from users.models import Client

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['client', 'ticket_number', 'seat_number', 'comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all()  # Populate clients
