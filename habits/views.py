
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from habits.models import Habit, CompletedDay
from habits.forms import CreateUpdateHabitForm


@login_required
def home_view(request):
    """
    Displays most recently updated habit if exists, otherwise redirects to 
    create habit page.
    """
    
    habit = Habit.objects.filter(owner=request.user, deleted=False
        ).order_by('updated_at').first()
    
    if habit:
        date_grid = habit.generate_grid()

        context = {
            'habit': habit,
            'date_grid': date_grid,
            'user_habits': Habit.objects.filter(owner=request.user, deleted=False)
        }

        return render(request, 'habits/habit.html', context)
    
    else:
        return redirect(reverse('create_habit'))


@login_required
def create_habit_view(request):
    """
    Renders create habit user interface on GET request, attempts to create 
    habit on POST request.
    """

    if not request.user.max_habits_created():
        form = CreateUpdateHabitForm()

        if request.method == 'POST':
            form = CreateUpdateHabitForm(request.POST)

            if form.is_valid():
                new_habit = form.save(commit=False)
                new_habit.owner = request.user
                new_habit.save()
                return redirect(reverse('habit', kwargs={'pk': new_habit.id}))

        context = {
            'form': form,
            'user_habits': Habit.objects.filter(owner=request.user, deleted=False),
        }
        
        return render(request, 'habits/create-habit.html', context)
    
    else:
        return redirect(reverse('max_habits_created'))
    

@login_required
def max_habits_created_view(request):
    """
    Renders warning to user that the max number of habits for the account has 
    been reached.
    """

    context = {
        'user_habits': Habit.objects.filter(owner=request.user, deleted=False),
    }

    return render(request, 'habits/max-habits-created.html', context)


@login_required
def habit_view(request, pk):
    """
    Renders the habit grid for the specified habit.
    """
    
    habit = get_object_or_404(Habit, id=pk, owner=request.user, deleted=False)
    date_grid = habit.generate_grid()

    context = {
        'habit': habit,
        'date_grid': date_grid,
        'user_habits': Habit.objects.filter(owner=request.user, deleted=False),
    }

    return render(request, 'habits/habit.html', context)


@login_required
def toggle_completed_day_view(request, pk):
    """
    Updates day grid cell via HTMX, removing CompletedDay if it already exists, 
    or creating it if it doesn't.
    """

    habit = get_object_or_404(Habit, id=pk, owner=request.user)

    try:
        existing_completed_day = CompletedDay.objects.get(
            habit=habit, 
            day=timezone.now().date()
        )
        existing_completed_day.delete()
        completed = False
    except ObjectDoesNotExist:
        CompletedDay.objects.create(
            habit = habit,
        )
        completed = True

    context = {
        'data': {
            'date': timezone.now().strftime('%Y-%m-%d'),
            'completed': completed,
            'is_past': False,
            'is_today': True,
        },
    }

    return render(request, 'habits/partials/day.html', context)