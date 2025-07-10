from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'base.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'index.html')
