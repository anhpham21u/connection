from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.new_post, name="newpost"),
    path('post/<str:id>/', views.post, name="post"),
    path('post/<str:id>/delete/', views.delete_post, name="delete_post"),
    path('post/<str:id>/comment/', views.send_comment, name="send_comment"),
    path('post/<int:id>/like_post/', views.like_post, name='like_post'),
    path('search/', views.search_view, name='search'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('latest_posts/', views.ListPostByTime.as_view(), name='latest_posts'),
    path('most_liked_posts/', views.ListPostByLike.as_view(), name='most_liked_posts'),
    path('posts/topic/<int:topic_id>/', views.ListPostByTopic.as_view(), name='post_by_topic'),
]