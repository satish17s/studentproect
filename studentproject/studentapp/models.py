from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    marks=models.PositiveIntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
