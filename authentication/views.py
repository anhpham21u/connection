from django.shortcuts import  render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def registration_view(request):
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