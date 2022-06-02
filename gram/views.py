from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

def index(request):
  title = 'Share your Story, Saa ni Sasa'
  template = 'gram/index.html'
  current_user = request.user
  
  context = {
    'title': title,
    'current_user': current_user,
  }
  
  return render(request, template, context)