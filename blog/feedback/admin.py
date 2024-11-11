from django.contrib import admin
from .models import Feedback
from .forms import FeedbackForm


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_item', 'rating', 'satisfaction', 'anonymous', 'date_created','comments')
    list_filter = ('rating', 'anonymous', 'date_created', 'satisfaction')  
    search_fields = ('user__username',) 
    ordering = ('-date_created',)  
    date_hierarchy = 'date_created'
    list_per_page = 10
    #autocomplete_fields = ('feedback_item',)
    
    
    

admin.site.register(Feedback,FeedbackAdmin)



