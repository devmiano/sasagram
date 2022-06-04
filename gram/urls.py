from . import views
from django.urls import include, path

urlpatterns = [
  path('', views.index, name='index'),
  path('auth/join/', views.join, name='join'),
  path('auth/login/', views.login, name='login'),
  path('auth/logout/', views.logout, name='logout'),
  path('profile/', views.profile, name='profile'),
]