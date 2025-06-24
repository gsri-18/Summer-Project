from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    
    name = models.CharField(max_length = 255)
    statement = models.TextField()
    code = models.CharField(max_length = 50, unique=True, default="TEMP")  # Unique identifier for the problem
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    time_limit = models.IntegerField(default = 1) # In seconds
    memory_limit = models.IntegerField(default = 128) # In MB

    def __str__(self):
        return self.name
    

class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"TestCase for {self.problem.name} - Input: {self.input[:30]}..."

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)  # e.g., 'Python', 'Java', etc.
    verdict = models.CharField(max_length = 50) 

    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.name} - Verdict: {self.verdict}"
    

