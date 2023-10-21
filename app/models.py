from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    pub_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text