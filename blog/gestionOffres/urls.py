from django.urls import path
from .views import *
from .views import offreListView, DetailsViewoffre
#from .views import ListViewOffre  # Assurez-vous que ListViewOffre est bien importé

urlpatterns = [
    
    path('listViewoffre/', offreListView.as_view(), name='listViewoffre'),

  
    path('details/<int:pk>/',DetailsViewoffre.as_view(),
         name="detailoffre"), #affiche une conference bien determine selon le nombre entree
    path('search/', search_offres, name='search_offres'),
    #path('<int:offre_id>/export_program_pdf/', export_program_pdf, name='export_program_pdf'),
    path('rate/<int:offre_id>/', rate_offre, name='rate_offre'),

    path('download_program/<int:offre_id>/', export_program_pdf, name='export_program_pdf'),

    

] 