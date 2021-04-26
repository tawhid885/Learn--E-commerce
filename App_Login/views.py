from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from django.http import HttpResponse


#Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 


#Models and Forms
from App_Login.models import Profile
from App_Login.forms import ProfileForm,SignUpForm


#Messages
from django.contrib import messages


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST' or request.method == 'post':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Your Account is Successfully Created!")
            # return HttpResponseRedirect(reverse('App_Login:login'))
            return redirect('App_Shop:home')
    return render(request,'App_Login/sign_up.html',context={'form':form})



def login_user(request):
    form =AuthenticationForm()
    if request.method == 'POST' or request.method == 'post':
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password = password)

            if user is not None:
                login(request,user)
                return redirect('App_Shop:home')
    return render(request,'App_Login/login.html',context={'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are Logged Out!")
    return redirect('App_Login:login')


@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST' or request.method == 'post':
        form = ProfileForm(request.POST,instance=profile)

        if form.is_valid():
            form.save()
            messages.info(request,"Profile Changed!")
            form = ProfileForm(instance=profile)
    
    return render(request,'App_login/change_profile.html',context={'form':form})


    