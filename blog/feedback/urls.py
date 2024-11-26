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


urlpatterns = [
    path('',  FeedbackListView.as_view(), name='feedback_list'),
    path('', FeedbackListView.as_view(), name='acceuil'),
    path('feedback_update/<int:id>/', views.feedback_update, name='feedback_update'),
    path('feedback_delete/<int:id>/', views.feedback_delete, name='feedback_delete'),
]


