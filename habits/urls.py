from django.urls import path

from habits import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('create-habit/', views.create_habit_view, name='create_habit'),
    path('max-habits-created/', views.max_habits_created_view, name='max_habits_created'),
    path('habit/<str:pk>/', views.habit_view, name='habit'),
    path('habit-day-toggle/<str:pk>/', views.toggle_completed_day_view, name='habit_completed_day_toggle'),    
]