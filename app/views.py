import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .forms import PostForm
from .models import Comment, Post
from django.db.models import Q

# Create your views here.
def index(req):
    posts = Post.objects.all()
    return render(req, 'app/index.html', {'posts': posts})

def post(req, id):
    post = Post.objects.get(id=id)
    comments = post.comments.all()
    comment_count = comments.count()
    return render(req, 'app/post.html', {'post': post, 'comments': comments, 'comment_count': comment_count})

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

def delete_post(request, id):
    post = Post.objects.get(id=id)

    if request.user == post.user:
        post.delete()
        return redirect('account')
    else:
        return redirect('account')
    

def like_post(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        user = request.user

        if user not in post.likes.all():
            post.likes.add(user)
            return JsonResponse({'message': 'Liked'})
        else:
            post.likes.remove(user)
            return JsonResponse({'message': 'Unliked'})
    return JsonResponse({'message': 'Invalid request'})

def send_comment(request, id):
    data = json.loads(request.body)
    textComment = data["textComment"]
    post = Post.objects.get(id=id)
    
    # Tạo một comment mới
    comment = Comment(user=request.user, text=textComment, post=post)
    comment.save()
    
    return JsonResponse({"message": "Comment sent successfully"})

def search_view(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'app/search_results.html', {'results': results, 'query': query})