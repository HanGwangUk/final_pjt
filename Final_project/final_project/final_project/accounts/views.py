from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
    
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')

    else:
        form = UserCreationForm()
    
    context= {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # return redirect('movies:index')
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    
    context ={
        'form' : form
    }

    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')