from django.test import TestCase
from problems.models import Problem

class ProblemModelTest(TestCase):
    def test_problem_creation(self):
        prob = Problem.objects.create(
            name="Sum of Two Numbers",
            code="SUM001",
            difficulty="Easy",
            time_limit=1.5,
            memory_limit=128,
        )
        self.assertEqual(str(prob), "Sum of Two Numbers (SUM001)")
        self.assertEqual(prob.difficulty, "Easy")
