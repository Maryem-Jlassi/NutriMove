# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render #pour afficher un template en passant un dictionnaire

from .models import offre
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect


#Utilité : Assurer que seules les personnes connectées peuvent voir la liste des conférences/ajouter/supp .. confer
#Si un utilisateur non connecté tente d'accéder à cette vue, il sera redirigé vers la page de connexion spécifiée par login_url="login"
#@login_required(login_url="login")






    
class offreListView(ListView):
    model=offre
    template_name ='offres/listOffre.html'
    context_object_name='offres' #permet d’accéder aux conférences sous le nom conferences dans le template.
    def get_queryset(self):
        return offre.objects.order_by('start_date')
    #urcharge la méthode pour trier les conférences par start_date en ordre croissant.
 

class DetailsViewoffre(DetailView):
    model=offre
    template_name='offres/detailsOffres.html'
    context_object_name ='offre'
    '''
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = self.get_object() # Récupère l'objet Conference actuellement consulté
        # Récupérer les réservations associées à cette conférence
        context['reservations'] = Reservation.objects.filter(conference=conference) #filtrage des reservation selon la conference selectionne et les mettre dans un contexte 
        return context
       #autrement  dit hne ki tenzli 3la details bch ykharejlk les reservations mt3 l conference heki 
    '''