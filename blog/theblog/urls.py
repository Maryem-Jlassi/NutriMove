from django.urls import path
from .views import *
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/comment/', create_comment, name='create_comment'),
    path('comment_update/<int:pk>/', update_comment, name='comment_update'),
    #path('comment_delete/<int:pk>/', DeleteCommentView.as_view(), name='comment_delete'),
    path('reply/add/<int:id>/', CreateReplyView.as_view(), name='create_reply'),
    path('like_post/<int:pk>/', like_post, name='like_post'),
     path('update-comment/<int:comment_id>/', update_comment, name='comment_update'),
     path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
     path('post/<int:pk>/pdf/', download_post_pdf, name='download_post_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
