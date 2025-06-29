from django.db import models

# Create your models here.
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
