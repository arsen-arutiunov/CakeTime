from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,
                              verbose_name="Email Address",
                              blank=False,
                              null=False)
    username = models.CharField(unique=True,
                                max_length=40,
                                verbose_name="User ID")
    first_name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(max_length=50, verbose_name="Surname")
    phone = models.CharField(max_length=20,
                             unique=True,
                             verbose_name="Phone",
                             blank=False,
                             null=False,
                             default="Empty")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    def __str__(self):
        return self.email if self.email else self.username
