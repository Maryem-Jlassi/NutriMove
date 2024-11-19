from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Validator function to allow only letters
def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError('This field can contain letters only.')

class post(models.Model):
    title = models.CharField(max_length=255, validators=[validate_letters_only])
    title_tag = models.CharField(max_length=255, default="sports blog")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    CHOICES = (
        ('sport', 'sport'),
        ('nutrition', 'nutrition'),
    )
    category = models.CharField(max_length=255, null=True, choices=CHOICES)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title + ' | ' + str(self.author)

class comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(
        validators=[MinLengthValidator(10), MaxLengthValidator(500)]
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)