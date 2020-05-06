from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from authentication.forms import *
from django.contrib import messages
# Create your views here.


def loginView(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            print("helloworld")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
                
            else:
                messages.info(request, 'Invalid Username or Password')
                form = LoginForm()
           
    else:
        form = LoginForm()   
    context = {
        'form': form
        
    }
    return render(request, 'registration/login.html', context)  

def logoutView(request):
    logout(request)
    return redirect('index')
      
           


def registerView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    context = {
        'form': form
    }   
    return render(request, 'registration/signup.html', context)    

   