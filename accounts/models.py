from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    roles = [("Elder", "Elder"), ("Youngster", "Youngster")]

    email = models.EmailField(unique = True)    
    role = models.CharField(max_length=10, choices=roles, default=None)

    REQUIRED_FIELDS = ('email', 'role')

    def __str__(self):
        return self.username


