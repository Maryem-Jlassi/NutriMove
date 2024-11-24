from django import forms
from .models import Participant
from users.models import Client

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        # Include only fields that are present in the Participant model
        fields = [
            'client',
            'ticket_number',
            'comments',
            'payment_status',
            'fitness_level'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all()  # Populate clients





from django import forms  # Add this import at the top of your file
from .models import Event

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'image', 'location', 'organizer', 'price', 'max_participants']

    # You can add custom form fields or validation if necessary

from django import forms

class EmailForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Choisir un client", to_field_name="email")
    
    title = forms.CharField(widget=forms.Textarea, label='Message', required=True)
    message = forms.CharField(widget=forms.Textarea, label='Message', required=True)
