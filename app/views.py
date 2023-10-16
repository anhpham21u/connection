from django.shortcuts import redirect, render
from .forms import PostForm
from .models import Post

# Create your views here.
def index(req):
    posts = Post.objects.all()
    return render(req, 'app/index.html', {'posts': posts})

def post(req, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        pass
    return render(req, 'app/post.html', {'post': post})

def new_post(request):
    user_log = request.user
    if not user_log.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'app/newpost.html', {'form': form})