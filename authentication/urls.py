from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_view, name="account"),
    path('login/', views.login_view, name="login"),
    path('register/', views.registration_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('change_password/', views.change_password, name="change_password"),
]