from django.db import models
from users.models import *

from django.core.exceptions import ValidationError

def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError('This field can contain letters only.')
class post(models.Model):
    title = models.CharField(max_length=255, validators=[validate_letters_only])
    title_tag = models.CharField(max_length=255,default="sports blog")
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    CHOICES=(
        ('sport','sport'),
        ('nutrition','nutrition'),
    )

    category=models.CharField(max_length=255, null=True,choices=CHOICES)
    picture=models.ImageField(null=True,blank=True,upload_to="images/")
    likes=models.ManyToManyField(User, related_name="likedposts" ,through="LikedPost")
    created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)


class LikedPost(models.Model):
    post=models.ForeignKey(post, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} : {self.post.title}'



class comment(models.Model):
    id = models.AutoField(primary_key=True)
    post=models.ForeignKey(post,related_name="comments", on_delete=models.CASCADE)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    body= models.TextField()    
    date_added= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' %(self.post.title,self.name)



class reply(models.Model):
    id = models.AutoField(primary_key=True)
    parent_comment=models.ForeignKey(comment,related_name="replies", on_delete=models.CASCADE)
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    body= models.TextField()    
    date_added= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        try:
            return f'{self.name} :{self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'
     

