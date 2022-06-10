from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

# Create your tests here.
class TestUser(TestCase):
  def setUp(self) -> None:
    self.example_user = User(username="miano", email="dev@miano.com", password="devmiano", password2="devmiano")
    self.example_user.save()

  def test_user_instance(self):
    self.assertTrue(isinstance(self.example_user, User))
    

class TestProfile(TestCase):
  def setUp(self) -> None:
    self.example_user = User(username="miano", email="dev@miano.com", password="devmiano", password2="devmiano")
    self.example_user.save()

    self.example_profile = Profile(id_user='11802', user=self.example_user, firstname="miano", lastname="miano", photo="media/default-user.svg", bio="This is a test profile")

  def test_profile_instance(self):
    self.assertTrue(isinstance(self.example_profile, Profile))
