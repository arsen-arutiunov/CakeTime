from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,
                              verbose_name="Email Address",
                              blank=False,
                              null=False)
    username = models.CharField(unique=True, max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
