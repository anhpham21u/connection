import json
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils import timezone
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
    
    #time
    current_time = timezone.now()
    time_difference = current_time - post.pub_date
    hours_difference = time_difference.total_seconds() / 3600
    days_difference = time_difference.days
    if days_difference > 0:
        time_ago = f"{days_difference} ngày trước"
    elif hours_difference >= 1:
        time_ago = f"{int(hours_difference)} giờ trước"
    else:
        minutes_difference = int(time_difference.total_seconds() / 60)
        time_ago = f"{minutes_difference} phút trước"

    return render(req, 'app/post.html', {'post': post, 'comments': comments, 'comment_count': comment_count, 'time_ago': time_ago})

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
    user_log = request.user
    if not user_log.is_authenticated:
        return redirect('login')

    post = Post.objects.get(id=id)
    user = request.user

    if user not in post.likes.all():
        post.likes.add(user)
        return redirect('post', id)
    else:
        post.likes.remove(user)
        return redirect('post', id)

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

def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES['file']

        if image_file:
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image_file.name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            with open(upload_path, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            image_url = os.path.join(settings.MEDIA_URL, 'uploads', image_file.name) 

            return JsonResponse({'url': image_url})

    return JsonResponse({'error': 'Image upload failed'}, status=400)
