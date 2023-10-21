import json
from django.views.generic import ListView
import os
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils import timezone
from .forms import PostForm
from .models import Comment, Post, Topic
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def index(request):
    posts = Post.objects.all()

    # pageination
    per_page = 10
    paginator = Paginator(posts, per_page)
    page = request.GET.get('page')

    try:
        posts = paginator.get_page(page)
    except EmptyPage:
        posts = paginator.get_page(1)

    current_page = posts.number
    total_pages = paginator.num_pages

    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    elif current_page <= 3:
        page_range = range(1, 6)
    elif current_page >= total_pages - 2:
        page_range = range(total_pages - 4, total_pages + 1)
    else:
        page_range = range(current_page - 2, current_page + 3)


    return render(request, 'app/index.html', {'posts': posts, 'page_range': page_range})

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
        time_ago = f"{days_difference} days ago"
    elif hours_difference >= 1:
        time_ago = f"{int(hours_difference)} hours ago"
    else:
        minutes_difference = int(time_difference.total_seconds() / 60)
        time_ago = f"{minutes_difference} minutes ago"

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

class ListPostByTime(ListView):
    model = Post
    template_name = 'app/list_post_time.html'
    context_object_name = 'list_post_time'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = self.request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except EmptyPage:
            posts = paginator.get_page(1)

        current_page = posts.number
        total_pages = paginator.num_pages

        if total_pages <= 5:
            page_range = range(1, total_pages + 1)
        elif current_page <= 3:
            page_range = range(1, 6)
        elif current_page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)

        context['page_range'] = page_range
        return context

class ListPostByLike(ListView):
    model = Post
    template_name = 'app/most_liked_posts.html'
    context_object_name = 'most_liked_posts'
    paginate_by = 10
    queryset = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = self.request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except EmptyPage:
            posts = paginator.get_page(1)

        current_page = posts.number
        total_pages = paginator.num_pages

        if total_pages <= 5:
            page_range = range(1, total_pages + 1)
        elif current_page <= 3:
            page_range = range(1, 6)
        elif current_page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)

        context['page_range'] = page_range
        return context

class ListPostByTopic(ListView):
    model = Post
    template_name = 'app/post_by_topic.html'
    context_object_name = 'post_by_topic'
    paginate_by = 10

    def get_queryset(self):
        topic_id = self.kwargs.get('topic_id')
        return Post.objects.filter(topic_id=topic_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id = self.kwargs.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        context['topic_name'] = topic.name

        paginator = context['paginator']
        page = self.request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except EmptyPage:
            posts = paginator.get_page(1)

        current_page = posts.number
        total_pages = paginator.num_pages

        if total_pages <= 5:
            page_range = range(1, total_pages + 1)
        elif current_page <= 3:
            page_range = range(1, 6)
        elif current_page >= total_pages - 2:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(current_page - 2, current_page + 3)

        context['page_range'] = page_range

        return context