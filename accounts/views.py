from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    """
    Display the registration page.
    """

    """
    register new user"""

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        #check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register") 
        
        if User.objects.filter(username=username).exists():
           messages.error(request, "Username already exists.")
           return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        #create new user
        User.objects.create_user(username=username, email=email, password=password)


        #redirect to login page after successful registration
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_user(request):
    """
    Login an existing user.
    """

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "accounts/login.html")

@login_required(login_url="login")
def profile(request):
    return render(request, "accounts/profile.html",
                  {"user": request.user})

@login_required(login_url="login")
def edit_profile(request):

    if request.method == "POST":
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
    return render(request, "accounts/edit_profile.html")