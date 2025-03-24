import uuid, random, string

from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.account.models import EmailAddress

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

    habit_limit = models.IntegerField(default=5)
    

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
        return self.all_habits.filter(deleted=False).count() >= self.habit_limit
    


class SignUpCode(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=12, unique=True, editable=False, null=True, blank=True)


    class Meta:
        ordering = ['created',]
        verbose_name = 'Signup Code'
        verbose_name_plural = 'Signup Codes'


    def __str__(self):
        return str(self.code)


    def save(self, *args, **kwargs):
        
        if self._state.adding and not self.code:
            self.code = self.generate_code()
        
        super(SignUpCode, self).save(*args, **kwargs)


    def generate_code(self, length=12):
        """
        Generate a unique signup code that a user requires to signup for the 
        app.
        """
        
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if not SignUpCode.objects.filter(code=code).exists():
                return code