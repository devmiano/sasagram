from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import *
from itertools import chain
import random

def index(request):
  title = 'Share your Story, Saa ni Sasa'
  template = 'gram/index.html'
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)
  follow_feed = []
  feed = []
  user_follow = Follow.objects.filter(follower=request.user.username)
  
  for users  in user_follow:
    follow_feed.append(users.user)
    
  for usernames in follow_feed:
    gram_feeds = Gram.objects.filter(user=usernames)
    feed.append(gram_feeds)
    
  gram_feed = list(chain(*feed))
  
  all_users = User.objects.all()
  all_user_following = []
  
  for user in user_follow:
    user_list = User.objects.get(username=user.user)
    all_user_following.append(user_list)
    
  user_suggestions = [x for x in list(all_users) if (x not in list(all_user_following))]
    
  current_user = User.objects.filter(username=request.user.username)
  new_suggestions = [x for x in list(user_suggestions) if (x not in list(current_user))]
  
  random.shuffle(new_suggestions)
  
  profile_feed = []
  profile_feeds = []
  
  for users in new_suggestions:
    profile_feed.append(users.id)
    
  for ids in profile_feed:
    users_feeds = Profile.objects.filter(id_user=ids)
    profile_feeds.append(users_feeds)
  
  suggestions_feed = list(chain(*profile_feeds))
  
  context = {
    'title': title,
    'grams': gram_feed,
    'suggestions': suggestions_feed[:5],
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
  follower = request.user.username
  user = pk
  
  if Follow.objects.filter(user=user, follower=follower).first():
    btn_txt = 'Unfollow'
  else:
    btn_txt = 'Follow'
    
    
  user_followers = len(Follow.objects.filter(user=pk))
  user_following = len(Follow.objects.filter(follower=pk))
  
  context = {
    'title': title,
    'btn_txt': btn_txt,
    'user_grams': user_grams,
    'total_grams': total_grams,
    'user_object': user_object,
    'user_profile': user_profile,
    'user_followers': user_followers,
    'user_following': user_following,
  }
  
  return render(request, template, context)


@login_required(login_url='login')
def settings(request):
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

@login_required(login_url='login')
def follow(request):
  if request.method == 'POST':
    follower = request.POST['follower']
    user = request.POST['user']
    
    if Follow.objects.filter(user=user, follower=follower).first():
      unfollowed = Follow.objects.get(user=user, follower=follower)
      unfollowed.delete()
      
      return redirect('/profile/'+user)
    
    else:
      followed = Follow.objects.create(user=user, follower=follower)
      followed.save()
      
      return redirect('/profile/'+user)
  else:
    return redirect('index')
  
@login_required(login_url='login')
def search(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)
  template = 'gram/search.html'
  title = 'Search'
  
  if request.method == 'POST':
    username = request.POST['username']
    username_obj = User.objects.filter(username__icontains=username)
    
    search_profile = []
    search_profile_feed = []
    
    for users in username_obj:
      search_profile.append(users.id)
      
    for ids in search_profile:
      profile_feeds = Profile.objects.filter(id_user=ids)
      search_profile_feed.append(profile_feeds)
      
    search_profile_feed = list(chain(*search_profile_feed))  
    
    context = {
      'title': title,
      'user_profile': user_profile,
      'search_profile_feed': search_profile_feed,
    }
    
  return render(request, template, context)