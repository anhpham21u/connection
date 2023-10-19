from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.new_post, name="newpost"),
    path('post/<str:id>/', views.post, name="post"),
    path('post/<str:id>/delete/', views.delete_post, name="delete_post"),
    path('post/<str:id>/comment/', views.send_comment, name="send_comment"),
    path('post/<int:id>/like_post/', views.like_post, name='like_post'),
    path('search/', views.search_view, name='search')
]