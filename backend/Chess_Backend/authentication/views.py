from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password, check_password

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Checking if username repeated
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already exists. Please choose a different one.')

        hashed_password = make_password(password)
        User.objects.create(username=username, password=hashed_password)
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return HttpResponse('Login Successful')
            else:
                return HttpResponse('Invalid Password')
        except User.DoesNotExist:
            return HttpResponse('User does not exist')

    return render(request, 'login.html')
