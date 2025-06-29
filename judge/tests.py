from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTest(TestCase):
    def test_home_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
