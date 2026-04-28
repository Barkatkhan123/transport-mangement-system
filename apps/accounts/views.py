from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm, PassengerProfileForm
from .models import PassengerProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.full_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_agency_manager:
                return redirect('agency:dashboard')
            if user.is_admin_user:
                return redirect('dashboard:admin')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')
    # Reject GET-based logout attempts silently
    return redirect('home')


@login_required
def profile_view(request):
    try:
        passenger_profile = request.user.passenger_profile
    except PassengerProfile.DoesNotExist:
        passenger_profile = None

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = PassengerProfileForm(request.POST, instance=passenger_profile) if passenger_profile else None

        if user_form.is_valid():
            user_form.save()
            if profile_form and profile_form.is_valid():
                profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        profile_form = PassengerProfileForm(instance=passenger_profile) if passenger_profile else None

    return render(request, 'auth/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)
