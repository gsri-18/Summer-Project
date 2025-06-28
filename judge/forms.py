from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problem, TestCase

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2'
        ]


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'name', 'code', 'difficulty', 'time_limit', 'memory_limit',
            'description', 'input_format', 'output_format', 'constraints',
            'sample_input', 'sample_output'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'memory_limit': forms.NumberInput(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'input_format': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'output_format': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'constraints': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'sample_input': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'sample_output': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }



from django import forms
from django.forms import inlineformset_factory
from .models import Problem, TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input', 'output']
        widgets = {
            'input': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'output': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

TestCaseFormSet = inlineformset_factory(
    Problem,
    TestCase,
    form=TestCaseForm,
    extra=1,
    can_delete=True
)


from django import forms
from .models import User

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    


