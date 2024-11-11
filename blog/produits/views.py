from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Produit
from .forms import ProduitForm  # Vous devrez créer ce formulaire
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render

def fitness_home(request):
    return render(request, 'fitness/index.html')

# Liste des produits
class ProduitListView(ListView):
    model = Produit
    template_name = 'produits/produit_list.html'
    context_object_name = 'produits'

# Détail d'un produit
class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'produits/produit_detail.html'

# Création d'un produit
class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

# Mise à jour d'un produit
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'produits/produit_form.html'
    success_url = reverse_lazy('produit_list')

# Suppression d'un produit
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'produits/produit_confirm_delete.html'
    success_url = reverse_lazy('produit_list')