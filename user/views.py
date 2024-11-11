# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# Register view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in!')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You logged in successfully!')
            return redirect('home')  # Redirect to home page after login
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


# Create your views here.
