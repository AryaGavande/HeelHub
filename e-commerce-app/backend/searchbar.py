from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    title = models.CharField(max_length=200)
    keywords = models.TextField()

    def __str__(self):
        return self.title
