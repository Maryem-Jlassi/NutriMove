from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from .models import post as Post
from .models import comment
from .models import reply # Changed to PascalCase for models
from .forms import commentForm , replyForm # Changed to PascalCase
from django.core.exceptions import PermissionDenied
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from PIL import Image as PILImage
from django.http import HttpResponse
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import post
from django.utils.timezone import localtime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.http import HttpResponse
from PIL import Image as PILImage
from django.utils.timezone import localtime
from reportlab.pdfgen import canvas

def translate_text(text: str, target_language="fr"):
    try:
        # Initialize the translation model pipeline
        pipe = pipeline("translation", model="google-t5/t5-base")
        # Perform translation
        translated = pipe(text, target_lang=target_language)
        return translated[0]['translation_text']
    except Exception as e:
        # Return error message in case of failure
        return f"Error: {str(e)}"
def translate_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        # Your translation logic here, e.g. using a translation service
        translated_body = translate_text(post.body)  # Implement your translation method
        
        return JsonResponse({
            'translated_body': translated_body
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = 'object_list'
    paginate_by = 10  

    def get_queryset(self):
    
        category_filter = self.request.GET.get('category', '')
        search_query = self.request.GET.get('search', '')
        sort_order = self.request.GET.get('sort', 'desc')  

        queryset = Post.objects.all()

     
        if category_filter:
            queryset = queryset.filter(category=category_filter)
       
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        if sort_order == 'asc':
            queryset = queryset.order_by('created')
        else:
            queryset = queryset.order_by('-created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
 
        context['categories'] = Post.objects.values_list('category', flat=True).distinct()

        context['paginator'] = context.get('paginator')
        context['page_obj'] = context.get('page_obj')

        return context


pipe = pipeline("summarization", model="facebook/bart-large-cnn")

# Alternatively, using AutoTokenizer and AutoModelForSeq2SeqLM
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
def summarize_article(request, post_id):
    # Get the post object
    post = get_object_or_404(Post, id=post_id)

    # Check if the content is long enough to summarize
    if len(post.body) > 100:
        # Tokenize the input text (post.body) and get input IDs
        inputs = tokenizer(post.body, return_tensors="pt", max_length=1024, truncation=True)

        # Generate the summary using the model
        summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=50, num_beams=4, early_stopping=True)

        # Decode the generated summary
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    else:
        summary_text = "The content is too short to summarize."

    # Return the summary as JSON
    return JsonResponse({"summary": summary_text})
class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_details.html"

    


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = comment
    form_class = commentForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
          
            post_instance = get_object_or_404(Post, pk=self.kwargs['pk'])

       
            form = self.form_class(request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post_instance
                new_comment.name = request.user  
                new_comment.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment added successfully!',
                    'comment': {
                        'id': new_comment.id,
                        'body': new_comment.body,
                        'name': new_comment.name.username,  
                        'date_added': new_comment.date_added.strftime('%B %d, %Y %H:%M'),
                    }
                })
            else:
               
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
                
        except Exception as e:
           
            return JsonResponse({
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}'
            }, status=500)

class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = comment
    template_name = 'create_comment.html'
    form_class = commentForm
    
    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.post.pk})
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied("You don't have permission to edit this comment.")
        return super().handle_no_permission()

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.post.pk})
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied("You don't have permission to delete this comment.")
        return super().handle_no_permission()
    
    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment deleted successfully!'
                })
            return response
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
            raise



def comment_delete(request, comment_id):
    if request.method == 'POST':
        try:
          
            Comment = comment  
            comment_obj = Comment.objects.get(id=comment_id)
            comment_obj.delete()
            return JsonResponse({
                'status': 'success', 
                'message': 'Comment deleted successfully'
            })
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class CreateReplyView(LoginRequiredMixin, CreateView):
    model = reply 
    form_class = replyForm  
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        try:
            parent_comment = get_object_or_404(comment, pk=self.kwargs['id'])
            form = self.form_class(request.POST)
            
            if form.is_valid():
                new_reply = form.save(commit=False)
                new_reply.parent_comment = parent_comment
                new_reply.name = request.user
                new_reply.post = parent_comment.post  
                new_reply.save()
                
                return JsonResponse({
                    'status': 'success',
                    'reply': {
                        'id': new_reply.id,
                        'body': new_reply.body,
                        'name': new_reply.name.username,
                        'date_added': new_reply.date_added.strftime('%B %d, %Y %H:%M')
                    }
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'errors': form.errors
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        





def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
        liked = True
    else:
        post.likes.remove(request.user)
        liked = False

    return JsonResponse({
        'status': 'success',
        'likes_count': post.likes.count(),
    })

def update_comment(request, comment_id):
    if request.method == 'POST':
        body = request.POST.get('body', None)
        if not body:
            return JsonResponse({'status': 'error', 'message': 'No comment body provided'})
        
        try:
           
            Comment = comment  
            comment_obj = Comment.objects.get(id=comment_id)
            comment_obj.body = body
            comment_obj.save()
            return JsonResponse({
                'status': 'success', 
                'message': 'Comment updated successfully',
                'comment': {
                    'id': comment_obj.id,
                    'body': comment_obj.body
                }
            })
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

'''
def download_post_pdf(request, pk):
    # Get the post
    post = get_object_or_404(Post, pk=pk)
    
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF document using ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Get the styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Add Header with Site Name
    header = Paragraph("Nutrimove Blog ", styles['Title'])
    story.append(header)
    story.append(Spacer(1, 12))
    
    # Add Title
    story.append(Paragraph(post.title, title_style))
    story.append(Spacer(1, 12))
    
    # Add Author with styling
    story.append(Paragraph(f"By: {post.author.username}", normal_style))  # using post.author.username to display author name
    story.append(Spacer(1, 12))
    
    # Add Date of Creation
    story.append(Paragraph(f"Published on: {localtime(post.created).strftime('%B %d, %Y')}", normal_style))
    story.append(Spacer(1, 12))
    
    # Add Category
    if post.category:
        story.append(Paragraph(f"Category: {post.category.capitalize()}", normal_style))
        story.append(Spacer(1, 12))
    
    # Add Body Content with word wrap
    story.append(Paragraph(post.body, normal_style))
    story.append(Spacer(1, 12))
    
    # Add image if it exists
    if post.picture:
        img_path = post.picture.path
        img = PILImage.open(img_path)
        aspect = img.height / float(img.width)
        
        # Set a maximum width for the image (e.g., 400 points)
        desired_width = 400
        desired_height = desired_width * aspect
        
        # Add the image to the PDF
        img = Image(img_path, width=desired_width, height=desired_height)
        story.append(img)
        story.append(Spacer(1, 12))
    
    # Add a footer with page number
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawString(200, 20, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    
    # Get the value of the BytesIO buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create the HTTP response with PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'
    response.write(pdf)
    
    return response'''

def download_post_pdf(request, pk):
    post = get_object_or_404(Post, pk=pk)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=75,
        bottomMargin=50,
    )
    story = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.darkblue,
        alignment=1, 
    )
    
 
    def add_header(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.darkblue)
        canvas.rect(0, letter[1] - 50, letter[0], 50, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(50, letter[1] - 35, "NutiMove ")
        canvas.restoreState()
    class FooterCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.pages = []

        def showPage(self):
            self.pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            for page in self.pages:
                self.__dict__.update(page)
                self.draw_footer()
                super().showPage()
            super().save()

        def draw_footer(self):
            self.saveState()
            self.setLineWidth(0.5)
            self.setStrokeColor(colors.grey)
            self.line(50, 40, letter[0] - 50, 40) 
            self.setFont("Helvetica", 10)
            self.setFillColor(colors.grey)
            self.drawCentredString(letter[0] / 2.0, 30, f"Page {self._pageNumber}")
            self.restoreState()

    story.append(Paragraph(post.title, title_style))
    story.append(Spacer(1, 20))
    
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=12,
    )
    story.append(Paragraph(f"By: {post.author.username}", meta_style))
    story.append(Paragraph(f"Published on: {localtime(post.created).strftime('%B %d, %Y')}", meta_style))
    
    if post.category:
        story.append(Paragraph(f"Category: {post.category.capitalize()}", meta_style))
        story.append(Spacer(1, 12))
   
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=18,  
    )
    story.append(Paragraph(post.body, body_style))
    story.append(Spacer(1, 20))
  
    if post.picture:
        img_path = post.picture.path
        img = PILImage.open(img_path)
        aspect = img.height / float(img.width)
        desired_width = 400
        desired_height = desired_width * aspect
        img = Image(img_path, width=desired_width, height=desired_height)
        story.append(Spacer(1, 12))
        story.append(img)
        story.append(Spacer(1, 20))
    
  
    story.append(PageBreak())
    doc.build(story, onFirstPage=add_header, onLaterPages=add_header, canvasmaker=FooterCanvas)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'
    response.write(pdf)
    
    return response
