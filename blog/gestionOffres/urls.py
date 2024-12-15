from django.urls import path
from .views import *
from .views import offreListView, DetailsViewoffre, analyze_face
#from .views import ListViewOffre  # Assurez-vous que ListViewOffre est bien importé

urlpatterns = [
    
    path('listViewoffre/', offreListView.as_view(), name='listViewoffre'),
    

  
    path('details/<int:pk>/',DetailsViewoffre.as_view(),
         name="detailoffre"), #affiche une conference bien determine selon le nombre entree
    path('search/', search_offres, name='search_offres'),
    #path('<int:offre_id>/export_program_pdf/', export_program_pdf, name='export_program_pdf'),
    path('rate/<int:offre_id>/', rate_offre, name='rate_offre'),

    path('download_program/<int:offre_id>/', export_program_pdf, name='export_program_pdf'),
    path('offre-statistics/', offre_statistics, name='offre_statistics'),
    path('offre-statistics-view/', offre_statistics_view, name='offre_statistics_view'),
    path('<int:offre_id>/lire/', lire_offre_vocale, name='lire_offre_vocale'),
    path('<int:offre_id>/lire/', lire_offre_vocale, name='lire_offre_vocale'),
    #path('<int:event_id>/analyze_face/', analyze_face, name='analyze_face'),
    path('analyze_face/', analyze_face, name='analyze_face')


] 