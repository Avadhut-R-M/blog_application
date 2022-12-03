from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from . import forms

# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return render(request, 'loggedin.html')
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return redirect('/home')
            else:
                message = 'Login failed!'
    return render(request, 'login.html', context={'form': form, 'message': message})

def signup(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            blog_add_permission = Permission.objects.get(codename='add_blog')
            user.user_permissions.add(blog_add_permission)
            user.is_staff = True
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    # request.user.session_set.all().delete()
    return redirect('/home')