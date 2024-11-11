from django.urls import path
from .views import ProduitListView, ProduitDetailView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView

urlpatterns = [
    path('', ProduitListView.as_view(), name='produit_list'),  # Liste des produits
    path('produit/nouveau/', ProduitCreateView.as_view(), name='produit_create'),  # Créer un nouveau produit
    path('produit/<str:pk>/', ProduitDetailView.as_view(), name='produit_detail'),  # Détails d'un produit
    path('produit/<str:pk>/modifier/', ProduitUpdateView.as_view(), name='produit_update'),  # Modifier un produit
    path('produit/<str:pk>/supprimer/', ProduitDeleteView.as_view(), name='produit_delete'),  # Supprimer un produit
]
