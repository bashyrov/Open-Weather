from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.views import get_weather, save_weekly_data
from main.models import City


def login(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('users:dashboard')
            else:
                form.add_error(None, "Invalid email or password.")
        else:
            form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('valid')
            return redirect('users:dashboard')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def dashboard(request):
    city = ''
    if request.user.users_city:
        city_name = request.user.users_city
        save_weekly_data(city_name)
        city = City.objects.filter(city_name=city_name).first()
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['users_city'].title()
            print(city_name)
            if get_weather(city_name, 'current'):
                form.save()
                return redirect('users:dashboard')
            else:
                form.add_error(None, "Please, provide a valid data.")
                messages.error(request, "Please, provide a valid data.")
        else:
            form.add_error(None, "Please, provide a valid data.")
            messages.error(request, "Please, provide a valid data.")
    else:
        form = UserProfileForm(instance=request.user)
        if request.user.users_city:
            get_weather(request.user.users_city, 'forecast')
    context = {
        'title': 'Dashboard',
        'username': request.user.username,
        'form': form,
        'city': city,
    }
    return render(request, 'users/dashboard.html', context)
