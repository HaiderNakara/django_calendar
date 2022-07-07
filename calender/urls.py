from django.urls import path

from . import views

urlpatterns = [
    path('init/', views.GoogleCalendarInitView, name='index'),
    path('redirect/', views.GoogleCalendarRedirectView, name='redirect'),
]
