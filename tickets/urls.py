
from . import views
from django.contrib import admin
from django.urls import path, include

app_name="tickets"

urlpatterns = [
    path('',views.ticketsIndex,name='ticketsIndex'),
  

] 