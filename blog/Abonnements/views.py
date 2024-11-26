from django.shortcuts import render
from .models import Abonnements
from .formuser import abonnementForm
from django.views.generic import CreateView
from django.urls import reverse_lazy ,reverse
from django.contrib.auth.views import LoginView,LogoutView
import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Client
from gestionOffres.models import offre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model

'''

class UserCreateView(CreateView):
    model=Client
    form_class =userForm
    template_name ="users/register.html"
    success_url = reverse_lazy('login')
'''
User = get_user_model()
    
  

def abonner_offre(request, offre_id):
    try:
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Vous devez être connecté pour vous abonner.'}, status=403)

        # Récupérer l'offre par ID
        selected_offre = get_object_or_404(offre, id=offre_id)

        # Vérifier que l'offre est toujours active (non expirée)
        if selected_offre.end_date < timezone.now().date():
            return JsonResponse({'error': 'Cette offre n\'est plus disponible.'}, status=400)

        # Vérifier qu'il n'y a pas déjà un abonnement pour le mois en cours
        start_of_month = timezone.now().replace(day=1)
        if Abonnements.objects.filter(participant=request.user, abonnement_date__gte=start_of_month).exists():
            return JsonResponse({'error': 'Vous avez déjà un abonnement ce mois-ci.'}, status=400)

        # Créer un nouvel abonnement
        abonnement = Abonnements.objects.create(
            offre=selected_offre,
            participant=request.user,  # L'utilisateur connecté est utilisé directement
            confirmed=True,
            abonnement_date=timezone.now()
        )

        return JsonResponse({'message': 'Abonnement réussi!', 'abonnement_id': abonnement.id}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
class LoginCustomView(LoginView):
    template_name='users/login.html'
    def get_success_url(self):
        return reverse('listViewoffre')