from django.contrib import admin
from .models import Feedback
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ( 'rating', 'anonymous', 'date_created','comments')
    list_filter = ('rating', 'anonymous', 'date_created')  
    search_fields = ('feedback_type',) 
    ordering = ('-date_created',)  
    date_hierarchy = 'date_created'
    list_per_page = 10
    

admin.site.register(Feedback,FeedbackAdmin)














