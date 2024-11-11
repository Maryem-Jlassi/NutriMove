from django.urls import path
from .views import *


urlpatterns=[ 
   # path('register/',UserCreateView.as_view(),name="register"),
    path('login/',LoginCustomView.as_view(),name="login"),
    #path('ajoutabonnement/<int:id>/', abonnementCreateView.as_view(), name="abonnement"),
   path('sabonner/<int:offre_id>/<int:user_id>/',abonner_offre,name="abonner"),
   ]