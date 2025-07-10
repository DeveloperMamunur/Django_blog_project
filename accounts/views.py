from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.
def register(request):
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save()
         login(request, user)
         return redirect('dashboard')
   else:
      form = UserCreationForm()
   return render(request, 'accounts/register.html', {'form': form})
   

def login_view(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect('dashboard')
   else:
      if request.user.is_authenticated:
         return redirect('dashboard')
   return render(request, 'accounts/login.html')

def logout_view(request):
   logout(request)
   return redirect('home')

@login_required(login_url='login')
def profile_settings(request):
   user = User.objects.get(username=request.user.username)
   profile, created = Profile.objects.get_or_create(user=request.user)

   context = {
      'user': user,
      'profile': profile,
   }
   return render(request, 'accounts/profile_settings.html', context)

@login_required(login_url='login')
def profile_picture_upload(request):
   if request.method == 'POST':
      user = User.objects.get(username=request.user.username)
      profile = Profile.objects.get(user=user)
      profile.profile_picture = request.FILES['profile_picture']
      profile.save()
      return redirect('profile_settings')
   return render(request, 'accounts/profile_settings.html')

def profile_picture_remove(request):
   user = User.objects.get(username=request.user.username)
   profile = Profile.objects.get(user=user)
   profile.profile_picture = None
   profile.save()
   return redirect('profile_settings')

@login_required(login_url='login')
def user_update(request):
   if request.method == 'POST':
      user = User.objects.get(username=request.user.username)
      user.first_name = request.POST.get('first_name')
      user.last_name = request.POST.get('last_name')
      user.username = request.POST.get('username')
      user.email = request.POST.get('email')
      user.save()
      return redirect('profile_settings')
   return render(request, 'accounts/profile_settings.html')

@login_required(login_url='login')
def profile_update(request):
   if request.method == 'POST':
      user = User.objects.get(username=request.user.username)
      profile = Profile.objects.get(user=user)
      profile.phone = request.POST.get('phone')
      profile.bio = request.POST.get('bio')
      profile.dob = request.POST.get('dob')
      profile.address = request.POST.get('address')
      profile.save()
      return redirect('profile_settings')
   return render(request, 'accounts/profile_settings.html')


@login_required
def password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user = request.user

        # Check if old password is correct
        if not user.check_password(old_password):
            messages.error(request, 'Your current password is incorrect.')
            return redirect('password_change')

        # Check new password match
        if password1 != password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('password_change')

        # Optional: add password strength validation here

        # Set new password
        user.set_password(password1)
        user.save()

        # Keep user logged in
        update_session_auth_hash(request, user)

        messages.success(request, 'Your password was changed successfully.')
        return redirect('password_change_success')
