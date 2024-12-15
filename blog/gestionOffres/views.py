
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
from users.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import offre, Client, Rating  # Import your models
from django.template.loader import render_to_string
#from weasyprint import HTML
import os
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Sum
import json
from django.http import HttpResponse
from gtts import gTTS
from django.core.files.storage import FileSystemStorage
from Abonnements.models import Abonnements 
import requests

#Utilité : Assurer que seules les personnes connectées peuvent voir la liste des conférences/ajouter/supp .. confer
#Si un utilisateur non connecté tente d'accéder à cette vue, il sera redirigé vers la page de connexion spécifiée par login_url="login"
#@login_required(login_url="login")
from transformers import pipeline
from events.models import Event

# Charger le modèle de résumé
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")





class offreListView(ListView):
    model = offre
    template_name = 'listOffre.html'
    context_object_name = 'offres'
    paginate_by = 3  # Number of offers per page

    def get_queryset(self):
        # Default sorting by start date
        queryset = offre.objects.order_by('start_date')
        
        # Optional: Add sorting based on GET parameters
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == 'titleOffre':
            queryset = queryset.order_by('titleOffre')
        
        return queryset
 

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




@login_required
def rate_offre(request, offre_id, user_id):
    try:
        # Fetch the offre object using get_object_or_404
        offre_instance = get_object_or_404(offre, id=offre_id)
        
        # Fetch the client instance using get_object_or_404
        client_instance = Client.objects.get(pk=user.pk)
        print(f"Client Instance: {client_instance}")  # This will output the client details in the console

        if request.method == 'POST':
            # Get the rating score from the POST data
            score = int(request.POST.get('score'))
            
            # Check if the user has already rated this offer
            existing_rating = Rating.objects.filter(offre=offre_instance, user=client_instance).first()
            
            if existing_rating:
                # Update the existing rating
                existing_rating.score = score
                existing_rating.save()
            else:
                # Create a new rating
                Rating.objects.create(offre=offre_instance, user=client_instance, score=score)

            # Redirect to the offer detail page
            return redirect('offre_detail', offre_id=offre_instance.id)

        # Render a template if not POST
        return render(request, 'listOffre.html', {'offre': offre_instance})
    
    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client non trouvé.'}, status=404)
    except offre.DoesNotExist:
        return JsonResponse({'error': 'Offre non trouvée.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def offre_statistics(request):
    """
    Fonction de vue pour générer des statistiques détaillées sur les offres
    """
    # Statistiques de base
    total_offres = offre.objects.count()
    average_price = offre.objects.aggregate(avg_price=Avg('price'))['avg_price']
    max_price = offre.objects.aggregate(max_price=Max('price'))['max_price']
    min_price = offre.objects.aggregate(min_price=Min('price'))['min_price']

    # Statistiques de capacité
    total_capacity = offre.objects.aggregate(total_capacity=Sum('capacity'))['total_capacity']
    average_capacity = offre.objects.aggregate(avg_capacity=Avg('capacity'))['avg_capacity']
    
    # Offres actives
    today = timezone.now().date()
    active_offres = offre.objects.filter(
        start_date__lte=today, 
        end_date__gte=today
    )

    # Offres à venir (dans les 30 prochains jours)
    future_date = today + timezone.timedelta(days=30)
    upcoming_offres = offre.objects.filter(
        start_date__range=[today, future_date]
    )

    # Offres expirées
    expired_offres = offre.objects.filter(end_date__lt=today)

    # Statistiques par coach
    coaches_offres = offre.objects.values('coach_id').annotate(
        coach_offre_count=Count('id'),
        coach_total_capacity=Sum('capacity')
    )

    # Statistiques par nutritionniste
    nutritionists_offres = offre.objects.values('nutrisionist_id').annotate(
        nutritionist_offre_count=Count('id'),
        nutritionist_total_capacity=Sum('capacity')
    )

    # Compilation des statistiques
    statistics = {
        'total_offres': total_offres,
        'pricing': {
            'average_price': round(average_price, 2) if average_price else 0,
            'max_price': max_price,
            'min_price': min_price
        },
        'capacity': {
            'total_capacity': total_capacity,
            'average_capacity': round(average_capacity, 2) if average_capacity else 0
        },
        'status': {
            'active_offres_count': active_offres.count(),
            'upcoming_offres_count': upcoming_offres.count(),
            'expired_offres_count': expired_offres.count()
        },
        'coaches': list(coaches_offres),
        'nutritionists': list(nutritionists_offres)
    }

    # Retourne les statistiques au format JSON
    return JsonResponse(statistics)

def offre_statistics_view(request):
    """
    Vue pour rendre les statistiques dans un template HTML
    """
    # Extraire les données de statistiques
    response = offre_statistics(request)  # Appel à la fonction qui retourne JsonResponse
    statistics = response.content  # Obtenir le contenu brut
    statistics = json.loads(statistics)  # Charger les données JSON en objet Python

    return render(request, 'offre_statistics.html', {'statistics': statistics})



def lire_offre_vocale(request, offre_id):
    # Récupérer l'offre spécifique à partir de l'ID
    offre_instance = get_object_or_404(offre, id=offre_id)
    
    # Créer le texte qui sera lu
    texte_a_lire = f"Le titre de cet offre est : {offre_instance.titleOffre}.La Capacité de cet offre est de l'ordre de: {offre_instance.capacity}, le Prix est : {offre_instance.price},Si vous voulez avoir plus d'informations,merci de faire telecharger le programme: {offre_instance.program}."
    
    # Convertir le texte en parole
    tts = gTTS(texte_a_lire, lang='fr')  # 'fr' pour la langue française
    
    # Créer un fichier temporaire pour sauvegarder l'audio
    fs = FileSystemStorage()
    audio_file_path = os.path.join(fs.location, f'offer_audio_{offre_id}.mp3')
    
    # Si un ancien fichier audio existe, le supprimer
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

    # Utiliser le 'with' pour s'assurer que le fichier est bien fermé après l'enregistrement
    with fs.open(f'offer_audio_{offre_id}.mp3', 'wb') as temp_file:
        tts.save(temp_file)  # Sauvegarder l'audio dans le fichier temporaire

    # Créer une réponse HTTP avec le fichier audio
    with open(audio_file_path, 'rb') as audio_file:
        response = HttpResponse(audio_file.read(), content_type='audio/mp3')
        response['Content-Disposition'] = f'inline; filename="offer_audio_{offre_id}.mp3"'

    return response


def analyze_face(request):
    """
    Analyse l'image téléchargée et retourne le résultat de l'analyse.
    Si un âge est prédit, des offres spécifiques sont récupérées.
    """
    response_message = None  # Variable pour stocker la réponse de l'API
    error_message = None  # Variable pour stocker les messages d'erreur
    filtered_offers = None  # Variable pour stocker les offres filtrées

    if request.method == "POST":
        image = request.FILES.get("image")  # Récupérer l'image téléchargée

        if image:
            # Préparer les données pour la requête POST
            files = {'image': image}
            headers = {
                "x-rapidapi-key": "f875700bacmshc39a326dde2ffc3p163701jsn487deac76591",
                "x-rapidapi-host": "face-analyzer1.p.rapidapi.com",
            }

            try:
                # Effectuer la requête POST vers l'API avec l'image
                api_url = "https://face-analyzer1.p.rapidapi.com/analyze/full"
                response = requests.post(api_url, files=files, headers=headers)

                # Vérifier si la requête est réussie
                if response.status_code == 200:
                    response_data = response.json()

                    # Affichage de la réponse brute pour vérifier la structure
                    print("Réponse brute de l'API : ", response_data)

                    # Accéder au premier élément de la liste 'data'
                    data = response_data.get("data", [{}])[0]  # Prendre le premier élément de la liste, ou un dictionnaire vide si vide

                    # Extraire les données
                    response_message = {
                        "age": data.get("age"),
                        "emotion": data.get("emotion"),
                        "gender": data.get("gender")
                    }

                    # Vérifier si des données valides sont présentes
                    if not response_message["age"]:
                        error_message = "L'API n'a pas pu analyser correctement l'image."
                    else:
                        # Si l'âge est valide, filtrer les offres en fonction de critères
                        age = response_message["age"]

                        # Déterminer la catégorie en fonction de l'âge
                        if age < 18:
                            category = 'kids'  # Catégorie pour les enfants
                        elif 18 <= age <= 32:
                            category = 'teens'  # Catégorie pour les adolescents
                        else:
                            category = 'other'  # Catégorie pour les autres tranches d'âge

                        # Filtrage des offres selon l'âge et la catégorie
                        if age < 18:
                            filtered_offers = offre.objects.filter(
                                category=category,  # Filtrer selon la catégorie 'kids'
                               
                            )
                        elif 18 <= age <= 32:
                            filtered_offers = offre.objects.filter(
                                category=category,  # Filtrer selon la catégorie 'teens'
                                
                            )
                        else:
                            filtered_offers = offre.objects.filter(
                                category=category,  # Filtrer selon la catégorie 'other'
                               
                            )

                        # Vérification si des offres ont été trouvées
                        if not filtered_offers:
                            error_message = "Aucune offre trouvée pour ces critères."

                else:
                    error_message = f"Erreur de l'API, code de statut : {response.status_code}"

            except Exception as e:
                error_message = f"Exception lors de l'appel à l'API : {str(e)}"

    # Afficher le résultat de l'analyse ou un message d'erreur, avec les offres filtrées si présentes
    return render(
        request,
        "face_analyzer.html",  # Modifiez le chemin si nécessaire
        {
            "response": response_message,
            "error": error_message,
            "filtered_offers": filtered_offers,  # Passer les offres filtrées au template
        }
    )