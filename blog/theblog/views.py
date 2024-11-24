from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import post ,comment
from .forms import *
from django.urls import reverse 
# Create your views here.
# def home(request):
#     return render (request, 'home.html' , {})

from django.shortcuts import get_object_or_404

class homeview(ListView):
    model =post
    template_name="home.html"



class article_detail_view(DetailView):
    model=post
    template_name="article_details.html"


class CreateViewcomment(CreateView):
    model=comment
    template_name='create_comment.html'
    form_class=commentForm
    #fields=['body'] 
    def get_success_url(self):
        return reverse('article_detail', args=[self.object.post.pk])
    
class UpdateViewcomment(UpdateView):
    model=comment
    template_name='create_comment.html' 
    form_class=commentForm
    def get_success_url(self):
        return reverse('article_detail', args=[self.object.post.pk])
    

class DeleteViewConference(DeleteView):
    model=comment
    template_name='comment_confirm_delete.html'
    def get_success_url(self):
        return reverse('article_detail', args=[self.object.post.pk])
    