
# Create your views here.
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render #pour afficher un template en passant un dictionnaire
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import offre,Rating,Client
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from reportlab.lib import colors
from django.template.loader import render_to_string
#from weasyprint import HTML
import os
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from .models import offre
#Utilité : Assurer que seules les personnes connectées peuvent voir la liste des conférences/ajouter/supp .. confer
#Si un utilisateur non connecté tente d'accéder à cette vue, il sera redirigé vers la page de connexion spécifiée par login_url="login"
#@login_required(login_url="login")






    
class offreListView(ListView):
    model=offre
    template_name ='listOffre.html'
    context_object_name='offres' #permet d’accéder aux conférences sous le nom conferences dans le template.
    def get_queryset(self):
        return offre.objects.order_by('start_date')
    #urcharge la méthode pour trier les conférences par start_date en ordre croissant.
 

class DetailsViewoffre(DetailView):
    model=offre
    template_name='detailsOffres.html'
    context_object_name ='offre'
   
   
def search_offres(request):
    query = request.GET.get('q')  # Récupère la valeur du champ "q" dans l'URL
    if query:
        offres = offre.objects.filter(titleOffre__icontains=query)  # Recherche insensible à la casse
    else:
        offres = offre.objects.all()  # Si aucun mot-clé n'est saisi, affiche toutes les offres

    return render(request, 'search_offres.html', {'offres': offres, 'query': query})


def export_program_pdf(request, offre_id):
    try:
        # Récupérer l'offre par son ID
        offre_instance = get_object_or_404(offre, id=offre_id)

        # Vérifier si un programme est attaché à l'offre
        if not offre_instance.program:
            return JsonResponse({'error': 'Aucun programme disponible pour cette offre.'}, status=404)

        # Récupérer le chemin complet du fichier program
        file_path = offre_instance.program.path

        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            raise SuspiciousOperation("Le fichier demandé est introuvable.")

        # Ouvrir et envoyer le fichier à l'utilisateur
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            # Définir le nom du fichier de téléchargement
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    except offre.DoesNotExist:
        return JsonResponse({'error': 'Offre non trouvée.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def list_offres(request):
    sort_by = request.GET.get('sort_by', 'price')  # Default sorting by price
    
    # Apply sorting based on the user's selection
    if sort_by == 'price':
        offres = offre.objects.all().order_by('price')  # Sort by price
    elif sort_by == 'start_date':
        offres = offre.objects.all().order_by('start_date')  # Sort by start_date
    elif sort_by == 'titleOffre':
        offres = offre.objects.all().order_by('titleOffre')  # Sort by titleOffre
    else:
        offres = offre.objects.all().order_by('price')  # Default to sorting by price
    
    return render(request, 'search_offres.html', {'offres': offres})



def rate_offre(request, offre_id=1, user_id=5):
    try:
        # Get the client instance
        client_instance = get_object_or_404(Client, pk=user_id)
        
        # Get the offre (offer) instance using offre_id
        offre_instance = get_object_or_404(offre, pk=offre_id)
        
        if request.method == 'POST':
            # Get the rating score from the form
            score = int(request.POST.get('score'))
            
            # Check if the user has already rated this offer
            existing_rating = Rating.objects.filter(offre=offre_instance, user=client_instance).first()
            
            if existing_rating:
                # Update existing rating
                existing_rating.score = score
                existing_rating.save()
            else:
                # Create new rating
                Rating.objects.create(offre=offre_instance, user=client_instance, score=score)

            # Redirect to the offer detail page
            return redirect('offre_detail', offre_id=offre_instance.id)  # Make sure 'offre_detail' URL uses 'offre_id'
        
        # If it's a GET request, render the offer detail page with the offer instance
        return render(request, 'listOffre.html', {'offre': offre_instance})
    
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client non trouvé.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)