from django.urls import path

from habits import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('habit/<str:pk>/', views.habit_view, name='habit'),
    path('create-habit/', views.create_habit_view, name='create_habit'),
    path('delete-habit/<str:pk>/', views.delete_habit_view, name='delete_habit'),
    path('max-habits-created/', views.max_habits_created_view, name='max_habits_created'),
]

htmx_patterns = [
    path('habit-day-toggle/<str:pk>/', views.toggle_completed_day_view, name='habit_completed_day_toggle'),
]

urlpatterns += htmx_patterns