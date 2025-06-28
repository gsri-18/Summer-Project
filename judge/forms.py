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

from django import forms
from .models import Problem
import bleach

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'

    def _sanitize_markdown_field(self, value):
        if not value:
            return ''
        # Step 1: Replace <br> tags with \n (even if bleach doesn't catch them)
        value = value.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
        # Step 2: Remove all other HTML tags
        return bleach.clean(value, tags=[], strip=True)

    def clean_description(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("description"))

    def clean_input_format(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("input_format"))

    def clean_output_format(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("output_format"))

    def clean_constraints(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("constraints"))

    def clean_sample_input(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("sample_input"))

    def clean_sample_output(self):
        return self._sanitize_markdown_field(self.cleaned_data.get("sample_output"))




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

    


