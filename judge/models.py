from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, default="TEMP")  # Unique identifier like "SUM001"
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    time_limit = models.IntegerField(default=1)  # seconds
    memory_limit = models.IntegerField(default=128)  # MB

    # NEW STRUCTURED FIELDS
    description = models.TextField()
    input_format = models.TextField(blank=True)
    output_format = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)

    def __str__(self):
        return self.name

    

class TestCase(models.Model):
    input = models.TextField()
    output = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')

    def __str__(self):
        return f"TestCase for {self.problem.name} - Input: {self.input[:30]}..."

from django.utils import timezone

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)  # e.g., 'Python', 'Java', etc.
    verdict = models.CharField(max_length = 50) 
    submitted_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.name} - Verdict: {self.verdict}"
    
from django.db import models
from django.conf import settings
from django.utils import timezone

class Contest(models.Model):
    title = models.CharField(max_length=100)
    code = models.SlugField(unique=True)  # e.g., W1, JUNE24, etc.
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    problems = models.ManyToManyField('Problem', related_name='contests')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_contests'
    )

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def is_upcoming(self):
        return timezone.now() < self.start_time

    def is_ended(self):
        return timezone.now() > self.end_time

    def __str__(self):
        return f"{self.title} ({self.code})"


class ContestSubmission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contest_submissions'
    )
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE,
        related_name='contest_submissions'
    )
    code = models.TextField()
    language = models.CharField(max_length=20)  # 'python', 'c', 'cpp', 'java'
    verdict = models.CharField(max_length=20, blank=True)  # 'AC', 'WA', etc.
    time_submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_submitted']
        unique_together = ('user', 'contest', 'problem', 'time_submitted')

    def __str__(self):
        return f"{self.user.username} - {self.problem.code} - {self.verdict}"

