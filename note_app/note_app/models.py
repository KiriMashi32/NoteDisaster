from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    

class Task(models.Model):
    content = models.TextField()
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)  # Nouveau champ