from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from store.models import CustomerModel


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Check if user is in database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('store')
        else:
            messages.success(request, ("Error logging in - Please try again..."))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('store')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            newUser = User.objects.filter(username=username).first()
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            CustomerModel.objects.create(user= newUser, name= firstName, surname=lastName, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered..."))
            return redirect('store')
    else:
        form = RegisterUserForm()
    return render(request, 'authentication/register_user.html', {'form': form})
