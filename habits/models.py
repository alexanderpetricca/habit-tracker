import uuid
from datetime import date, timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):

    DURATION_CHOICES = (
        (7, '7'),
        (14, '14'),
        (30, '30'),
        (60, '60'),
        (120, '120'),
        (365, '365'),
    )

    id = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        primary_key=True, 
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='all_habits',
    )
    name = models.CharField(max_length=50)
    duration = models.IntegerField(
        default=30,
        choices=DURATION_CHOICES,
        validators=[
            MinValueValidator(7),
            MaxValueValidator(365)
        ]
    )
    complete = models.BooleanField(default=False)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.name
    

    def generate_grid(self) -> dict:
        start_date = self.created_at.date()
        today = date.today()
        completed_days = set(self.completed_days.values_list("day", flat=True))

        date_grid = {
            (start_date + timedelta(days=i)): {
                "date": (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                "completed": (start_date + timedelta(days=i) in completed_days),
                "is_past": (start_date + timedelta(days=i)) < today,
                "is_today": (start_date + timedelta(days=i)) == today,
            }
            for i in range(self.duration)
        }

        return date_grid


    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


class CompletedDay(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        primary_key=True, 
        editable=False,
    )
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='completed_days',
    )
    day = models.DateField(auto_now_add=True)


    def __str__(self):
        return str(self.day)

