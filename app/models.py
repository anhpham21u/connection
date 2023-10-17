from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title