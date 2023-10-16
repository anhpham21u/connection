from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages

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