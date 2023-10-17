from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.new_post, name="newpost"),
    path('post/<str:id>/', views.post, name="post"),
    path('post/<str:id>/delete/', views.delete_post, name="delete_post"),
    path('like_post/<int:id>/', views.like_post, name='like_post')
]