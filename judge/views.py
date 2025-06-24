from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission

from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.http import HttpResponse


# Create your views here.

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems.html', {'problems': problems})

@login_required
def problem_detail(request, code):

    problem = get_object_or_404(Problem, code=code)
    verdict = None


    if request.method == 'POST':
        submitted_code = request.POST.get('code')
        language = request.POST.get('language')
        user = request.user

        submission = Submission.objects.create(
            problem=problem,
            code=submitted_code,
            language=language,
            verdict="Pending..", # hardcoded now, later real Docker verdict
            user=user
        )

        verdict = submission.verdict

    return render(request, 'problem_detail.html', {
        'problem': problem,
        'verdict': verdict,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def home_view(request):
    return HttpResponse("<h1>Welcome to CodeVerse!</h1><p><a href='/register/'>Register</a> | <a href='/admin/'>Admin</a> | <a href='/problems/'>Problems</a></p>")
