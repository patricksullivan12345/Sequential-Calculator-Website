from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from users.models import Profile
from .forms import CustomUserCreationForm, ProfileForm

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        print('You are signed in')
        return redirect('projects')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    print("You are logged out")
    return redirect('projects')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('projects')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'register.html', context)

@login_required(login_url="login")
def deleteProfile(request, **kwargs):

    print('Delete profile signal triggered')

    try:
        user = request.user
        user.delete()
    except:
        pass
        
    context = post_delete.connect(deleteProfile, sender=Profile)
    
    if not request.user.is_authenticated:
        return redirect('home')

    logout(request)

    return render(request, 'delete_profile.html', context)

@login_required(login_url="login")
def user_profile(request):

    user_data = request.user.profile

    context = {"user_data":user_data}

    return render(request, 'view_profile.html', context)

@login_required(login_url="login")
def editAccount(request):

    profile = request.user.profile

    current_user = request.user

    autofill = {'user':current_user}

    form = ProfileForm(autofill,instance=profile) 

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('view_profile')

    context = {'form': form}
    return render(request, 'edit_profile.html', context)