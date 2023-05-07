from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flashcard(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    hard_to_remember = models.IntegerField(default=0)
    time_cooldown = models.IntegerField(default=0)
    current_bin = models.CharField(max_length=200, default='bin0')
    last_bin_change = models.DateTimeField(default='2000-01-01 00:00:00.000000+00:00')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)