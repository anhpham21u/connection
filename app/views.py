from django.shortcuts import render
from .models import Post

# Create your views here.
def index(req):
    posts = Post.objects.all()
    return render(req, 'app/index.html', {'posts': posts})

def post(req, id):
    return render(req, 'app/post.html', {'id': id})
