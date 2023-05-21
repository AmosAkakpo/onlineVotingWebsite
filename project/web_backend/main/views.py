from .models import UserAnswer
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
import csv

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import random


def LoginPage(request):
    if request.method == 'POST':
        usern = request.POST.get('uname')
        pass1 = request.POST.get('userEnterPassword')
        User = authenticate(request, username=usern, password=pass1)
        if User is not None:
            # generate a random OTP and send it to the user's email address
            theOtp = random.randint(100000, 999999)
            send_mail(
                'Your OTP for Stra-X',
                f'Your OTP is {theOtp}.',
                settings.EMAIL_HOST_USER,
                [User.email],
                fail_silently=False,
            )
            # store the OTP in the session
            request.session['otp'] = theOtp
            # redirect the user to the OTP verification page
            return redirect('otp.html')
        else:
            # show an error message if the username and password are incorrect
            return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    else:
        # show the login form
        return render(request, 'login.html')


def OtpVerification(request):
    if request.method == 'POST':
        # get the OTP from the form
        otp = request.POST['otp']
        # get the OTP from the session
        session_otp = request.session.get('otp')
        if otp == str(session_otp):
            # delete the OTP from the session
            del request.session['otp']
            # log the user in using Django's built-in login function
            login(request, User)
            # redirect the user to the home page
            return redirect


@login_required(login_url='otp')
def HomePage(request):
    username = request.user.first_name
    context = {'username': username}
    return render(request, 'home.html', context)


def VotingPage(request):

    if request.method == 'POST':
        # Get the form data
        user_id = request.POST.get('user_id')
        city = request.POST.get('city')
        candidate = request.POST.get('candidate')

        # Save the data to a CSV file
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([user_id, city, candidate])

        # Render a success message
        return render(request, 'success.html')
    else:
        # Render the form template
        return render(request, 'voting.html')


def SignUpPage(request):
    if request.method == 'POST':
        unewid = request.POST.get('uId')
        ufirstname = request.POST.get('fname')
        ulastname = request.POST.get('lname')
        ucity = request.POST.get('city')
        uemail = request.POST.get('theEmail')
        upassword = request.POST.get('psw')

        User = get_user_model()
        my_user = User.objects.create_user(
            username=unewid, email=uemail, password=upassword)
        my_user.first_name = ufirstname
        my_user.last_name = ulastname
        my_user.city = ucity
        my_user.save()

        return redirect('login')

    return render(request, 'signup.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')
