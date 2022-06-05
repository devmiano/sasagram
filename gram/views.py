from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Gram, Like, Profile

def index(request):
  title = 'Share your Story, Saa ni Sasa'
  template = 'gram/index.html'
  user_object = User.objects.filter(username=request.user.username).first()
  user_profile = Profile.objects.filter(user=user_object).first()
  feed = Gram.objects.order_by('-posted').all()
  
  
  context = {
    'feed': feed,
    'title': title,
    'user_profile': user_profile,
  }
  
  return render(request, template, context)

def join(request):
  title = 'Get Started'
  template = 'gram/auth/join.html'
  
  context = {
    'title': title,
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
        
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)
        
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        
        return redirect('settings')
    
    else:
      messages.info(request, 'Passwords do not match')
      return redirect('join')
  
  else:
    return render(request, template, context)


def login(request):
  title = 'Welcome'
  template = 'gram/auth/login.html'
  
  context = {
    'title': title,
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

@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  return redirect('login')

@login_required(login_url='login')
def profile(request, pk):
  template = 'gram/profile/profile.html'
  
  user_object = User.objects.get(username=pk)
  user_profile = Profile.objects.get(user=user_object)
  user_grams = Gram.objects.filter(user=pk)
  total_grams = len(user_grams)
  title = f'{user_profile.user.username}'
  
  context = {
    'title': title,
    'user_grams': user_grams,
    'total_grams': total_grams,
    'user_object': user_object,
    'user_profile': user_profile,
  }
  
  return render(request, template, context)


@login_required(login_url='login')
def settings(request, pk):
  title = f'Update Profile'
  template = 'gram/profile/settings.html'
  user_profile = Profile.objects.get(user=request.user)
  
  if request.method == 'POST':
    if request.FILES.get('photo') == None:
      photo = user_profile.photo
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      bio = request.POST['bio']
      
      
      user_profile.photo = photo
      user_profile.firstname = firstname
      user_profile.lastname = lastname
      user_profile.bio = bio
      user_profile.save()
      
      
    if request.FILES.get('photo') != None:
      photo = request.FILES.get('photo')
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      bio = request.POST['bio']
      
      
      user_profile.photo = photo
      user_profile.firstname = firstname
      user_profile.lastname = lastname
      user_profile.bio = bio
      user_profile.save()
      
    return redirect('index')

  context = {
    'title': title,
    'user_profile': user_profile,
  }
  return render(request, template, context)


@login_required(login_url='login')
def create(request, pk):
  user_profile = Profile.objects.get(user=request.user)
  if request.method == 'POST':
    user = request.user.username
    photo = request.FILES.get('photo')
    title = request.POST['title']
    caption = request.POST['caption']
    profile = user_profile
    
    new_gram = Gram.objects.create(title=title, caption=caption, user=user, photo=photo, profile=profile)
    new_gram.save()
    
    return redirect('index')
  
  else:
    template = 'gram/profile/create.html'
    title = 'Create a new Post'
    
  
  context = {
    'title': title,
  }
  
  return render(request, template, context)


@login_required(login_url='login')
def like(request):
  username = request.user.username
  gram_id = request.GET.get('gram_id')
  gram = Gram.objects.get(id=gram_id)
  gram_like = Like.objects.filter(gram_id=gram_id, username=username).first()
  
  if gram_like is None:
    new_like = Like.objects.create(gram_id=gram_id, username=username)
    new_like.save()
    gram.likes = gram.likes+1
    gram.save()
    return redirect('index')
  
  else:
    gram_like.delete()
    gram.likes = gram.likes-1
    gram.save()
    return redirect('index')

