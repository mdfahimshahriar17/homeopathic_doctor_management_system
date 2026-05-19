from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'users/home.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.add_message(request, messages.SUCCESS, 'Invalid Username or Password')

    
    else:
        form = AuthenticationForm
    
    return render(request, 'users/users_auth_form.html', {'form' : form})

def user_logout(request):
    logout(request)
    return redirect('landing_page')