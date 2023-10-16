from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('newpost/', views.new_post, name="newpost"),
    path('post/<str:id>/', views.post, name="post")
]