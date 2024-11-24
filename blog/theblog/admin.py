from django.contrib import admin
from .models import post,comment,reply,LikedPost
# Register your models here.




admin.site.register(post)
admin.site.register(comment)
admin.site.register(reply)
admin.site.register(LikedPost)