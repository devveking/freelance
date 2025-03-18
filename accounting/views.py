from django.contrib.auth import login
from django.shortcuts import render


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm  # LoginForm уже создавали выше
from django.contrib import messages  # Для flash-сообщений

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounting/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Заменить на нужный URL
        else:
            messages.error(request, 'Неверный email или пароль')
    else:
        form = CustomLoginForm()
    return render(request, 'accounting/login.html', {'form': form})


def show_home(request):
    return render(request, 'home.html')

def show_profile(request):
    return render(request, 'profile.html')