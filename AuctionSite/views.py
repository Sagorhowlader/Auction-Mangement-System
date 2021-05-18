from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CreateUserForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.user.is_authenticated:
        return redirect('Auctions:AuctionSite')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('Auctions:AuctionSite')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'Login/login.html', context)



def UserRegistration(request):
    if request.user.is_authenticated:
        return redirect('Auctions:AuctionSite')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request,'Registrations/registrations.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')
