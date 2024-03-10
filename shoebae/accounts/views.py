from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

# Create your views here.
def register(request):
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if (password1 == password2):
            if (User.objects.filter(username=username).exists()):
                print("username taken, please try again...")
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,
                                            username=username,email=email,password=password1)
                user.save()
                print("User successfully created.")
        else:
            print("Password mismatch, please try again...")
            return redirect('/')
        return redirect('/') #change this redirect to login page
    else:
        return render(request,'register.html')