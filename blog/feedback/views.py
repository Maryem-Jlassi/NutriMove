from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from .models import Feedback
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.conf import settings

#create
def feedback_page(request):
    feedbacks = Feedback.objects.all().order_by('-date_created')
    paginator = Paginator(feedbacks, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = FeedbackForm(request.POST or None)
    star_range = list(range(1, 6))
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Sauvegarde du formulaire dans la base de données
            form.save()
            messages.success(request, "Votre feedback a été soumis avec succès !")
            return redirect('feedback_list')  # Redirige vers la liste des feedbacks
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = FeedbackForm()
    return render(request, 'feedbackpage.html', {'feedbacks': feedbacks, 'page_obj': page_obj,'star_range': star_range,'form': form})
'''
class CreateViewFeedback(CreateView):
    model = Feedback
    template_name = 'feedbackpage.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        messages.success(self.request, "Merci pour votre retour ! Votre feedback a été soumis.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('acceuil')  

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedbackpage.html'  # Le template où la liste des feedbacks sera affichée
    context_object_name = 'feedbacks'  # Nom de la variable dans le template
    paginate_by = 3  # Nombre d'éléments par page

    def get_queryset(self):
        return Feedback.objects.all()

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedbackpage.html'

    def form_valid(self, form):
        form.instance.user = self.request.user if self.request.user.is_authenticated else None
        messages.success(self.request, "Merci pour votre retour ! Votre feedback a été soumis.")
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Feedback ajouté avec succès.")
        return reverse_lazy('feedback') 
def FeedbackCreateView(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedbackpage.html', {'form': form})
    '''
#update
def feedback_update(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback mis à jour avec succès.")
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedbackpage.html', {'form': form, 'feedback': feedback})

def feedback_delete(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback supprimé avec succès.")
        return redirect('feedback_list')
    
def virtual_nutritionist(request):
    return redirect('upload_food_image')
    #return render(request, 'upload_food_image')





'''def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')  
    date_filter = request.GET.get('date_filter')
    rating_filter = request.GET.get('rating_filter')
    recent_feedbacks = Feedback.objects.all().order_by('-created_at')[:5]
    for feedback in feedbacks:
        feedback.stars = [i for i in range(feedback.rating)] 

    satisfaction_filter = request.GET.get('satisfaction_filter', '')

    if satisfaction_filter :
        feedbacks = Feedback.objects.filter(satisfaction=satisfaction_filter)
    else:
        feedbacks = Feedback.objects.all()

    if date_filter == 'last_week':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=7))
    elif date_filter == 'last_month':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=30))
    elif date_filter == 'last_year':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=365))

    if rating_filter:
        feedbacks = feedbacks.filter(rating=rating_filter)
        
    paginator = Paginator(feedbacks, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'satisfaction_filter': satisfaction_filter,
        'date_filter': date_filter,
        'rating_filter': rating_filter,
        'recent_feedbacks': recent_feedbacks,
        'feedbacks':feedbacks,
    }
    return render(request, 'feedbackpage.html' ,context)'''



from django.conf import settings
from .utils import classify_food, generate_fitness_tip, convert_to_audio
import uuid
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


def process_food_image(request):
    if request.method == 'POST' and 'food_image' in request.FILES:
        try:
            # Handle uploaded image
            food_image = request.FILES['food_image']
            
            # Generate a unique filename to avoid conflicts
            unique_filename = f"{uuid.uuid4()}{os.path.splitext(food_image.name)[1]}"
            
            # Save the image using FileSystemStorage
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            file_path = fs.save(unique_filename, food_image)
            image_url = fs.url(file_path)  # URL to serve the image
            
            # Classify the image
            detected_food = classify_food(fs.path(file_path))
            
            # Generate a fitness tip
            fitness_tip = generate_fitness_tip(detected_food)
            
            # Create an audio file for the tip
            audio_file_name = "fitness_tip.mp3"
            audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file_name)
            convert_to_audio(fitness_tip, filename=audio_file_path)
            audio_url = f"{settings.MEDIA_URL}{audio_file_name}" if os.path.exists(audio_file_path) else None
            
            # Return results to the template
            return render(request, 'upload_food_image.html', {
                'image_url': image_url,
                'detected_food': detected_food,
                'fitness_tip': fitness_tip,
                'audio_url': audio_url,
            })
        except Exception as e:
            print(f"Error processing the image: {e}")
            return render(request, 'upload_food_image.html', {
                'error': 'An error occurred while processing your image. Please try again.'
            })
    return render(request, 'upload_food_image.html')

              
'''

import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .utils import classify_food, generate_fitness_tip, convert_to_audio

def process_food_image(request):
    if request.method == 'POST' and 'food_image' in request.FILES:
        try:
            # Gérer l'image téléchargée
            food_image = request.FILES['food_image']
            fs = FileSystemStorage()
            file_path = fs.save(food_image.name, food_image)
            full_file_path = fs.path(file_path)  # Chemin absolu de l'image sauvegardée
            image_url = fs.url(file_path)  # URL pour afficher l'image dans le template
            
            # Classifier l'image
            detected_food = classify_food(full_file_path)
            
            # Générer un conseil fitness
            fitness_tip = generate_fitness_tip(detected_food)
            
            audio_file_name = "fitness_tip.mp3"
            audio_file_path = os.path.join(settings.BASE_DIR, 'feedback', 'static', audio_file_name)  # Sauvegarder dans 'static'
            convert_to_audio(fitness_tip, filename=audio_file_path)
            audio_url = f"{settings.STATIC_URL}{audio_file_name}"  # Utiliser STATIC_URL pour les fichiers dans 'static'

            if not audio_url:
                audio_url = "Error generating audio."
            
            # Renvoyer les résultats au template
            return render(request, 'upload_food_image.html', {
                'image_url': image_url,
                'detected_food': detected_food,
                'fitness_tip': fitness_tip,
                'audio_url': audio_url,
            })
        except Exception as e:
            print(f"Erreur lors du traitement de l'image : {e}")
            return render(request, 'upload_food_image.html', {
                'error': 'Une erreur est survenue lors du traitement de votre image. Veuillez réessayer.'
            })

    return render(request, 'upload_food_image.html')
'''