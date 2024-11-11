from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from .models import Feedback
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


def acceuil(request):
    feedbacks = Feedback.objects.filter(rating=5).order_by('-created_at')[:4]
    for feedback in feedbacks:
        feedback.stars = range(feedback.rating)
    return render(request, 'acceuil.html', {'feedbacks': feedbacks})

#creat
class CreateViewFeedback(CreateView):
    model = Feedback
    template_name = 'feedback_create.html'
    form_class = FeedbackForm


    def get_success_url(self):
        messages.success(self.request, "Merci pour votre retour ! Votre évaluation a été soumise avec succès.")
        return reverse_lazy('feedback_list')


# Liste des feedbacks avec filtres et pagination
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    date_filter = request.GET.get('date_filter')
    rating_filter = request.GET.get('rating_filter')
    satisfaction_filter = request.GET.get('satisfaction_filter', '')

    # Filtrer par satisfaction
    if satisfaction_filter:
        feedbacks = feedbacks.filter(satisfaction=satisfaction_filter)

    # Filtrer par date
    if date_filter == 'last_week':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=7))
    elif date_filter == 'last_month':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=30))
    elif date_filter == 'last_year':
        feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=365))

    # Filtrer par note
    if rating_filter:
        feedbacks = feedbacks.filter(rating=rating_filter)

    paginator = Paginator(feedbacks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_feedbacks = Feedback.objects.all().order_by('-created_at')[:5]

    context = {
        'page_obj': page_obj,
        'satisfaction_filter': satisfaction_filter,
        'date_filter': date_filter,
        'rating_filter': rating_filter,
        'recent_feedbacks': recent_feedbacks,
        'num_pages': paginator.num_pages,  
        'current_page': page_obj.number,  
    }
    return render(request, 'feedback_list.html', context)

# Mise à jour de feedback
def feedback_update(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre Feedback a été mise à jour avec succès.")
            return redirect('feedback_list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback_update.html', {'form': form, 'feedback': feedback})

# Suppression de feedback
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback supprimé avec succès!")
        return redirect('feedback_list')
    return render(request, 'feedback_delete.html', {'feedback': feedback})





