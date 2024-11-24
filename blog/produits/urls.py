from django.urls import path
from .views import ProduitListView, ProduitDetailView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView,add_achat,payment_success,payment_error
from . import views


urlpatterns = [
    path('', ProduitListView.as_view(), name='produit_list'),  # Liste des produits
    path('produit/nouveau/', ProduitCreateView.as_view(), name='produit_create'),  # Créer un nouveau produit
    path('produit/<str:reference>/', ProduitDetailView.as_view(), name='produit_detail'),  # Détails d'un produit
    path('achat/<str:produit_reference>/', views.add_achat, name='add_achat'),
    path('payment/execute/<int:achat_id>/', views.execute_payment, name='execute_payment'),
    path('produit/success/', views.payment_success, name='payment_success'),
    path('payment/error/', views.payment_error, name='payment_error'),
    path('produit/<str:pk>/modifier/', ProduitUpdateView.as_view(), name='produit_update'),  # Modifier un produit
    path('produit/<str:pk>/supprimer/', ProduitDeleteView.as_view(), name='produit_delete'),  # Supprimer un produit
    
]
