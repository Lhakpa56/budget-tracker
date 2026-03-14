from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Account created.")
            return redirect("dashboard")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")
