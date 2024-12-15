'''from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', views.acceuil, name="acceuil"),
    path('feedbackpage/' ,FeedbackListView.as_view(),name='feedback_list'),
    path('feedbackpage/', CreateViewFeedback.as_view(), name='feedback_create'),
    path('feedbackpage/<int:pk>/', views.feedback_update, name='feedback_update'),
    path('feedbackpage/<int:pk>/', views.feedback_delete, name='feedback_delete'),
]

'''


from django.urls import path
from . import views
from .views import *
from .views import process_food_image
from django.conf.urls.static import static


urlpatterns = [
  #  path('',  FeedbackListView.as_view(), name='acceuil'),
 #   path('', FeedbackListView.as_view(), name='acceuil'),
    path('', views.feedback_page, name='feedback_list'),  # Afficher et créer des feedbacks
    #path('', FeedbackListView.as_view(), name='feedback_list'),  # Liste des feedbacks
    #path('feedback/create/', views.FeedbackCreateView, name='feedback_create'),
    path('feedback_update/<int:id>/', views.feedback_update, name='feedback_update'),
    path('feedback_delete/<int:id>/', views.feedback_delete, name='feedback_delete'),
    path('process_food_image/', views.process_food_image, name='process_food_image'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

