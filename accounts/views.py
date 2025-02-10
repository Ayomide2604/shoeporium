from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            response = HttpResponse(status=200)
            response['HX-Redirect'] = '/'
            return response

        else:
            messages.error(
                request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Registration successful! You can now log in.')
            if request.headers.get('HX-Request'):
                return redirect('login')
            return redirect('login')
        else:
            messages.error(
                request, 'Registration failed. Please check the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully!')
        response = HttpResponse(status=204)
        response['HX-Redirect'] = '/'
        return response


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
