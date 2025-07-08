from django.contrib.auth.models import AbstractUser
from django.db import models
from problems.models import Problem, TestCase
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    full_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



from django.utils import timezone

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)  # e.g., 'Python', 'Java', etc.
    verdict = models.CharField(max_length = 50) 
    submitted_at = models.DateTimeField(default=timezone.now)
    code_file_path = models.TextField(blank=True, null=True)  # Path to the code file if stored


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
    problems = models.ManyToManyField(Problem, related_name='contests')
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
        Problem,
        on_delete=models.CASCADE,
        related_name='contest_submissions'
    )
    code = models.TextField()
    language = models.CharField(max_length=20)  # 'python', 'c', 'cpp', 'java'
    verdict = models.CharField(max_length=20, blank=True)  # 'AC', 'WA', etc.
    time_submitted = models.DateTimeField(auto_now_add=True)
    code_file_path = models.TextField(blank=True, null=True)  # Path to the code file if stored

    class Meta:
        ordering = ['time_submitted']
        unique_together = ('user', 'contest', 'problem', 'time_submitted')

    def __str__(self):
        return f"{self.user.username} - {self.problem.code} - {self.verdict}"
    

class DailyAICall(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date} -> {self.count}"

