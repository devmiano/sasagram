from . import views
from django.urls import path

urlpatterns = [
  path('', views.index, name='index'),
  path('auth/join/', views.join, name='join'),
  path('auth/login/', views.login, name='login'),
  path('auth/logout/', views.logout, name='logout'),
  path('<str:pk>/create/', views.create, name='create'),
  path('profile/<str:pk>/', views.profile, name='profile'),
  path('settings/', views.settings, name='settings'),
  path('like', views.like, name='like'),
  path('follow', views.follow, name='follow'),
  path('search/', views.search, name='search'),
]