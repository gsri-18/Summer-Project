from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problem, TestCase


class RegisterForm(UserCreationForm):
    class Meta:
        model  = User 
        fields = ['username', 'email', 'password1', 'password2']


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'name', 'code', 'difficulty', 'time_limit', 'memory_limit',
            'description', 'input_format', 'output_format', 'constraints',
            'sample_input', 'sample_output'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'input_format': forms.Textarea(attrs={'rows': 2}),
            'output_format': forms.Textarea(attrs={'rows': 2}),
            'constraints': forms.Textarea(attrs={'rows': 2}),
            'sample_input': forms.Textarea(attrs={'rows': 2}),
            'sample_output': forms.Textarea(attrs={'rows': 2}),
        }

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input', 'output']
        widgets = {
            'input': forms.Textarea(attrs={'rows': 2}),
            'output': forms.Textarea(attrs={'rows': 2}),
        }

TestCaseFormSet = forms.inlineformset_factory(
    Problem, TestCase, form=TestCaseForm,
    extra=2, can_delete=True
)
