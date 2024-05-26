from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_date = models.CharField(null=True, blank=True)
    born_location = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'"{self.text}" - {self.author.name}'


class CustomUser(AbstractUser):
    pass
