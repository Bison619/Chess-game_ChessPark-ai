from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('update_points/', views.update_points, name='update_points'),
    path('get_leaderboard/', views.get_leaderboard, name='get_leaderboard'),
]