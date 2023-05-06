from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    hard_to_remember = models.IntegerField(default=0)
    time_cooldown = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)