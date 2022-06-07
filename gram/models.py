import uuid
import cloudinary
from django.db import models
from datetime import datetime
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
  id_user = models.IntegerField()
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  bio = models.TextField(max_length=2000, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  photo = cloudinary.models.CloudinaryField('image')
  created = models.DateTimeField('date created', default = timezone.now)
  updated = models.DateTimeField('date updated', default=timezone.now)
  
  def __str__(self):
    return self.user.username
  
class Like(models.Model):
  gram_id = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  
  def __str__(self):
    return self.username
  
class Follow(models.Model):
  user = models.CharField(max_length=255)
  follower = models.CharField(max_length=255)
  
  def __str__(self):
    return self.user
  
class Comment(models.Model):
  gram_id = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  caption = models.TextField(max_length=2000)
  
  def save_comment(self):
    self.save()

  def delete_comment(self):
    self.delete()
  
  def __str__(self):
    return self.caption


class Gram(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  title = models.CharField(max_length=200)
  caption = models.TextField(max_length=2000)
  photo = cloudinary.models.CloudinaryField('image')
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
  posted = models.DateTimeField('date published', default=timezone.now)
  updated = models.DateTimeField('date updated', default=timezone.now)
  comments = models.ManyToManyField(Comment, related_name="grams")
  likes = models.IntegerField(default=0)
  user = models.CharField(max_length=200)
  
  def save_gram(self):
    self.save()

  def delete_gram(self):
    self.delete()

  def __str__(self):
    return self.title
  