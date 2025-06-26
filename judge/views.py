from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Problem, Submission
from .forms import RegisterForm

from pathlib import Path
import uuid
import subprocess
import shutil
import re
from django.conf import settings

ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}

# --- Utility Function ---
def run_code_util(code, language, input_data, base_path,
                  time_limit=1, memory_limit=128):
    uid = str(uuid.uuid4())
    base_path = Path(base_path)
    code_dir = base_path / 'code'
    input_dir = base_path / 'input'
    output_dir = base_path / 'output'
    code_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    if language not in ext_map:
        return {'error': 'Unsupported language'}

    filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
    code_path = code_dir / filename
    input_path = input_dir / f"input_{uid}.txt"
    output_path = output_dir / f"output_{uid}.txt"

    code_path.write_text(code)
    input_path.write_text(input_data)

    try:
        # --- Compilation ---
        if language in ['c', 'cpp']:
            exe_path = base_path / f"a_{uid}.out"
            compile_cmd = ['gcc', str(code_path), '-o', str(exe_path)] if language == 'c' else ['g++', str(code_path), '-o', str(exe_path)]
            result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                return {'error': 'Compilation Error', 'details': result.stderr.decode()}

        elif language == 'java':
            compile_cmd = ['javac', '-d', str(code_dir), str(code_path)]
            result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                return {'error': 'Compilation Error', 'details': result.stderr.decode()}

        elif language == 'python':
            try:
                compile(code, filename, 'exec')
            except SyntaxError as e:
                return {'error': 'Compilation Error', 'details': str(e)}

        # --- Execution ---
        with input_path.open('r') as infile, output_path.open('w') as outfile:
            if language == 'python':
                run_cmd = ['python3', str(code_path)]
                run_dir = None
            elif language in ['c', 'cpp']:
                run_cmd = [str(exe_path)]
                run_dir = None
            elif language == 'java':
                run_cmd = ['java', f'-Xmx{memory_limit}m', '-cp', str(code_dir), 'Main']
                run_dir = str(code_dir)

            run_cmd_str = (
                " ".join(run_cmd) if language == 'java'
                else f'ulimit -v {memory_limit * 1024}; timeout {time_limit} {" ".join(run_cmd)}'
            )

            result = subprocess.run(run_cmd_str, stdin=infile, stdout=outfile,
                                    stderr=subprocess.PIPE, timeout=time_limit + 1, cwd=run_dir, shell=True)

        stderr = result.stderr.decode().strip().lower()
        if result.returncode == 137 or 'outofmemoryerror' in stderr or 'killed' in stderr:
            return {'error': 'Memory Limit Exceeded'}
        elif result.returncode == 139 or 'segmentation fault' in stderr:
            return {'error': 'Runtime Error'}
        elif result.returncode != 0:
            return {'error': 'Runtime Error', 'details': stderr}

        output = output_path.read_text().strip()
        return {'output': output}

    except subprocess.TimeoutExpired:
        return {'error': 'Time Limit Exceeded'}

    finally:
        delete_toggle = (
            settings.DELETE_RUN_FILES_AFTER_EXECUTION if 'runs' in str(base_path) else
            settings.DELETE_SUBMISSION_FILES_AFTER_EVALUATION
        )
        if delete_toggle:
            shutil.rmtree(base_path, ignore_errors=True)

# --- Views ---
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems.html', {'problems': problems})


@login_required
def problem_detail(request, code):
    problem = get_object_or_404(Problem, code=code)
    verdict = None

    if request.method == 'POST':
        submitted_code = request.POST.get('code')
        language = request.POST.get('language', '').lower()
        user = request.user
        testcases = problem.testcases.all()

        if not testcases.exists():
            return HttpResponse("No test cases available for this problem.", status=400)

        uid = str(uuid.uuid4())
        base_path = Path(settings.BASE_DIR) / 'submission_files' / 'submissions' / f"{language}_{uid}"

        verdict = 'Accepted'
        for tc in testcases:
            result = run_code_util(
                submitted_code, language, tc.input, base_path,
                time_limit=problem.time_limit,
                memory_limit=problem.memory_limit
            )

            if 'error' in result:
                verdict = result['error']
                break

            normalized_output = re.sub(r'\s+', ' ', result['output'].strip())
            expected_output = re.sub(r'\s+', ' ', tc.output.strip())
            if normalized_output != expected_output:
                verdict = 'Wrong Answer'
                break

        submission = Submission.objects.create(
            user=user, problem=problem,
            code=submitted_code, language=language,
            verdict=verdict
        )
        return redirect('submission_detail', id=submission.id)

    return render(request, 'problem_detail.html', {'problem': problem, 'verdict': verdict})


@csrf_exempt
@login_required
def run_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    code = request.POST.get('code', '')
    language = request.POST.get('language', '').lower()
    custom_input = request.POST.get('custom_input', '')

    uid = str(uuid.uuid4())
    base_path = Path(settings.BASE_DIR) / 'submission_files' / 'runs' / f"{language}_{uid}"

    result = run_code_util(code, language, custom_input, base_path)
    return JsonResponse(result)


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
    return render(request, 'home.html')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('problem_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def submission_detail(request, id):
    submission = get_object_or_404(Submission, id=id)
    return render(request, 'submission_detail.html', {'submission': submission})


# --- Admin: Add Problem ---
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProblemForm, TestCaseFormSet

@staff_member_required
def add_problem_view(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        formset = TestCaseFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            problem = form.save()
            testcases = formset.save(commit=False)
            for tc in testcases:
                tc.problem = problem
                tc.save()
            return redirect('problem_detail', code=problem.code)
    else:
        form = ProblemForm()
        formset = TestCaseFormSet()

    return render(request, 'add_problem.html', {
        'form': form,
        'formset': formset,
    })


# --- Admin: Promote Users ---
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def promote_users_view(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")  # either promote or demote

        try:
            user = User.objects.get(id=user_id)
            if action == "promote":
                user.is_staff = True
                messages.success(request, f"{user.username} promoted to admin.")
            elif action == "demote":
                user.is_staff = False
                messages.success(request, f"{user.username} demoted to regular user.")
            user.save()
        except User.DoesNotExist:
            messages.error(request, "User not found.")
        return redirect("promote-users")

    return render(request, "promote_users.html", {"users": users})

