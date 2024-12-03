from django.db import models
from django.contrib.auth.models import User



class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

