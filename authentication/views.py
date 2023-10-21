from django.shortcuts import  render, redirect
from django.contrib import messages

from app.models import Post
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

def registration_view(request):
    user_log = request.user
    if user_log.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            if 'username' in form.errors:
                messages.error(request, "This username is already in use. Please choose a different one.")
            if 'email' in form.errors:
                messages.error(request, "This email is already in use. Please choose a different one.")
    form = NewUserForm()
    return render (request=request, template_name="authentication/register.html", context={"register_form":form})

def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    user_log = request.user
    if user_log.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="authentication/login.html", context={"login_form":form})

def account_view(request):
    user_log = request.user
    if not user_log.is_authenticated:
        return redirect('index')
    
    user = request.user
    posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'authentication/account.html', context)

def change_password(request):
    user_log = request.user
    if not user_log.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        print('test')
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Some thing went wrong!!!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/change_password.html', {'form': form})
