from django.urls import path
from .views import homeview, article_detail_view,CreateViewcomment,DeleteViewConference,UpdateViewcomment
from django.views.generic import RedirectView
urlpatterns = [
    #path('', RedirectView.as_view(url='/home/', permanent=False)),  # Redirects root URL to /home
    path('home/', homeview.as_view(), name="home"),
    path('article/<int:pk>/', article_detail_view.as_view(), name="article_detail"),
    path('create/<int:pk>/',CreateViewcomment.as_view(),name="comment_create"),
    path('delete/<int:pk>/',DeleteViewConference.as_view(),name="comment_delete"),
    path('update/<int:pk>/',UpdateViewcomment.as_view(), name='comment_update'),
]