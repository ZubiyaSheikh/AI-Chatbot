from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
            return render(request, "accounts/register.html", {"error": "Passwords do not match."})  
        
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {"error": "Username already exists."}) 
        
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {"error": "Email already exists."})
        
        #create new user
        User.objects.create_user(username=username, email=email, password=password)

        #redirect to login page after successful registration
        return redirect("login")
    
    return render(request, "accounts/register.html")


def login_user(request):
    """
    Login an existing user.
    """

    if request.method == "POST":

        # Get form data
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        # If username and password are correct
        if user is not None:

            # Log the user in
            login(request, user)

            # Redirect to chatbot
            return redirect("home")

        # Invalid username or password
        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")