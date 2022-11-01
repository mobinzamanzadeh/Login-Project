from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Login import settings


# Create your views here.


def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # username = request.POST['username']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        # email = request.POST['email']
        # pass1 = request.POST['pass1']
        # pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist !')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered !')
            return redirect('home')

        if len(username) < 7 or len(username) > 12:
            messages.error(request, 'The username must be between 7 and 12 characters')

        if len(pass1) < 10 or len(pass1) > 15:
            messages.error(request, 'The password must be between 10 and 15 characters')
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, 'Password did not match')
            return redirect('home')

        if not username.isalnum():
            messages.error(request, 'Username must be Alpha-Numeric !')
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, 'You are registered')

        # welcome message
        subject = 'Welcome to my web app - Django Login !'
        message = "Hello" + myuser.first_name + "! \n" + "Thanks for your register ! \n\n" + "Mobin Zamanzadeh"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return redirect('login')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})

        else:
            messages.error(request, "Invalid")
            return redirect('home')

    return render(request, 'login.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('home')
