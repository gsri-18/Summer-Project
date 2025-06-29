from django.test import TestCase
from judge.models import Submission, Problem, User

class SubmissionModelTest(TestCase):
    def test_submission_linked(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        prob = Problem.objects.create(
            name="Add",
            code="ADD001",
            difficulty="Easy",
            time_limit=1.0,
            memory_limit=128,
        )
        sub = Submission.objects.create(
            user=user,
            problem=prob,
            language="Python",
            code="print(sum(map(int, input().split())))",
            verdict="Accepted"
        )
        self.assertEqual(sub.verdict, "Accepted")
        self.assertIn("print", sub.code)
