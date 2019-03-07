from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_verify = request.POST['password_verify']

        if not email or not username or not first_name or not last_name or not password or not password_verify:
            return render(request, 'accounts/signup.html', {'error': 'Missing field. Please make sure everything has been filled.'})
        if password == password_verify:
            try:
                User.objects.get(username=username)
                return render(request, 'accounts/signup.html', {'error': 'There is already a user with that username.'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Your password verification did not match.'})
    else:
        return render(request, 'accounts/signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        email = username
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('home')
        return render(request, 'accounts/login.html', {'error': 'Unable to login'})
    else:
        return render(request, 'accounts/login.html')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
