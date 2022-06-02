from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
  id_user = models.IntegerField()
  bio = models.TextField(max_length=2000, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  photo = models.ImageField(upload_to = 'profile/', default='default-user.svg')
  created = models.DateTimeField('date created', default = timezone.now)

  def __str__(self):
    return self.user.username
  