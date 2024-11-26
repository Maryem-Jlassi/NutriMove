from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from .models import Feedback
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView

#create
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
'''
#read
class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        feedbacks = Feedback.objects.all().order_by('-date_created')
        # Filtrage par date, évaluation, etc.
        date_filter = self.request.GET.get('date_filter')
        rating_filter = self.request.GET.get('rating_filter')

        if date_filter == 'last_week':
            feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=7))
        elif date_filter == 'last_month':
            feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=30))
        elif date_filter == 'last_year':
            feedbacks = feedbacks.filter(date_created__gte=timezone.now() - timedelta(days=365))
        if rating_filter:
            feedbacks = feedbacks.filter(rating=rating_filter)
        

        return feedbacks
    # Méthode pour traiter la soumission du formulaire
    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user if request.user.is_authenticated else None
            feedback.save()
            messages.success(request, "Merci pour votre retour ! Votre feedback a été soumis.")
            return redirect('feedback_list')  # Redirige vers la même page pour voir le nouveau feedback

        # En cas d'erreur de validation, on réaffiche le formulaire avec les erreurs
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeedbackForm()  # Ajoutez le formulaire de création
        context['star_range'] = range(1, 6) 
        return context


#update

def feedback_update(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback mis à jour avec succès.")
            return redirect('acceuil')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback_list.html', {'form': form, 'feedback': feedback})

def feedback_delete(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, "Feedback supprimé avec succès.")
        return redirect('acceuil')








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










