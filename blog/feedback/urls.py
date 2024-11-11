from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', views.acceuil, name="acceuil"),
    path('feedback_list/' ,views.feedback_list,name='feedback_list'),
    path('feedback_create/', CreateViewFeedback.as_view(), name='feedback_create'),
    path('feedback_update/<int:pk>/', views.feedback_update, name='feedback_update'),
    path('feedback_delete/<int:pk>/', views.feedback_delete, name='feedback_delete'),
]

