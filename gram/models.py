import uuid
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
  id_user = models.IntegerField()
  bio = models.TextField(max_length=2000, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  photo = models.ImageField(upload_to = 'profile/', default='default-user.svg')
  created = models.DateTimeField('date created', default = timezone.now)
  updated = models.DateTimeField('date updated', default=timezone.now)
  
  def __str__(self):
    return self.user.username


class Gram(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  title = models.CharField(max_length=200)
  caption = models.TextField(max_length=2000)
  photo = models.FileField(upload_to='grams/%y/')
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  posted = models.DateTimeField('date published', default=timezone.now)
  updated = models.DateTimeField('date updated', default=timezone.now)
  likes = models.IntegerField(default=0)
  comments = models.IntegerField(default=0)
  user = models.CharField(max_length=200)
     
  def __str__(self):
    return self.title
  