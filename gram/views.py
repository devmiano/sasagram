from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Profile

def index(request):
  title = 'Share your Story, Saa ni Sasa'
  template = 'gram/index.html'
  current_user = request.user
  
  context = {
    'title': title,
    'current_user': current_user,
  }
  
  return render(request, template, context)

def join(request):
  title = 'Start your Journey'
  template = 'gram/auth/join.html'
  current_user = request.user
  
  context = {
    'title': title,
    'current_user': current_user,
  }
  
  if request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.info(request, 'This username is already taken')
        return redirect('join')
      
      elif User.objects.filter(email=email).exists():
        messages.info(request, 'This email already exists')
        return redirect('join')
      
      else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        
        return redirect('login')
    
    else:
      messages.info(request, 'Passwords do not match')
      return redirect('join')
  
  else:
    return render(request, template, context)

def login(request):
  title = 'Welcome Back'
  template = 'gram/auth/login.html'
  current_user = request.user
  
  context = {
    'title': title,
    'current_user': current_user,
  }
  
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
      auth.login(request, user)
      return redirect('index')
    
    else:
      messages.info(request, 'Authentication failed')
      return redirect('login')
    
  else:
    return render(request, template, context)

