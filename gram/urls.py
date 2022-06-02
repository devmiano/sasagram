from . import views
from django.urls import include, path

urlpatterns = [
  path('', views.index, name='index'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/', include('django_registration.backends.one_step.urls')),
]