from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('company/<slug:slug>/', views.company_detail, name='company_detail'),
    path('company/<slug:slug>/event/<int:event_id>/', views.event_detail, name='event_detail'),
]
