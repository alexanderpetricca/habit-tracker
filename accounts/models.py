import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
  
    id = models.UUIDField(
        default=uuid.uuid4, 
        unique=True, 
        editable=False, 
        primary_key=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    username = None
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['first_name',]
        verbose_name = "User"
        verbose_name_plural = "Users"


    def __str__(self):
        return f'{self.email}'
    

    def max_habits_created(self):
        if self.all_habits.all().count() >= 3:
            return True
        else:
            return False