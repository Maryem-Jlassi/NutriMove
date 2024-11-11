from django.urls import path
from .views import *
from .views import offreListView, DetailsViewoffre
#from .views import ListViewOffre  # Assurez-vous que ListViewOffre est bien importé

urlpatterns = [
    
    path('listViewoffre/', offreListView.as_view(), name='listViewoffre'),

  
    path('details/<int:pk>/',DetailsViewoffre.as_view(),
         name="detailoffre"), #affiche une conference bien determine selon le nombre entree

    

]