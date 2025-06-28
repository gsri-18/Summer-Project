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
import platform

ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}

# --- Utility Function ---
# def run_code_util(code, language, input_data, base_path,
#                   time_limit=1, memory_limit=128):
#     uid = str(uuid.uuid4())
#     base_path = Path(base_path)
#     code_dir = base_path / 'code'
#     input_dir = base_path / 'input'
#     output_dir = base_path / 'output'
#     code_dir.mkdir(parents=True, exist_ok=True)
#     input_dir.mkdir(parents=True, exist_ok=True)
#     output_dir.mkdir(parents=True, exist_ok=True)

#     if language not in ext_map:
#         return {'error': 'Unsupported language'}

#     filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
#     code_path = code_dir / filename
#     input_path = input_dir / f"input_{uid}.txt"
#     output_path = output_dir / f"output_{uid}.txt"

#     code_path.write_text(code)
#     input_path.write_text(input_data)

#     try:
#         # --- Compilation ---
#         if language in ['c', 'cpp']:
#             exe_path = base_path / f"a_{uid}.out"
#             compile_cmd = ['gcc', str(code_path), '-o', str(exe_path)] if language == 'c' else ['g++', str(code_path), '-o', str(exe_path)]
#             result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             if result.returncode != 0:
#                 return {'error': 'Compilation Error', 'details': result.stderr.decode()}

#         elif language == 'java':
#             compile_cmd = ['javac', '-d', str(code_dir), str(code_path)]
#             result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             if result.returncode != 0:
#                 return {'error': 'Compilation Error', 'details': result.stderr.decode()}

#         elif language == 'python':
#             try:
#                 compile(code, filename, 'exec')
#             except SyntaxError as e:
#                 return {'error': 'Compilation Error', 'details': str(e)}

#         # --- Execution ---
#         with input_path.open('r') as infile, output_path.open('w') as outfile:
#             if language == 'python':
#                 run_cmd = ['python3', str(code_path)]
#                 run_dir = None
#             elif language in ['c', 'cpp']:
#                 run_cmd = [str(exe_path)]
#                 run_dir = None
#             elif language == 'java':
#                 run_cmd = ['java', f'-Xmx{memory_limit}m', '-cp', str(code_dir), 'Main']
#                 run_dir = str(code_dir)

#             run_cmd_str = (
#                 " ".join(run_cmd) if language == 'java'
#                 else f'ulimit -v {memory_limit * 1024}; timeout {time_limit} {" ".join(run_cmd)}'
#             )

#             result = subprocess.run(run_cmd_str, stdin=infile, stdout=outfile,
#                                     stderr=subprocess.PIPE, timeout=time_limit + 1, cwd=run_dir, shell=True)

#         stderr = result.stderr.decode().strip().lower()
#         if result.returncode == 137 or 'outofmemoryerror' in stderr or 'killed' in stderr:
#             return {'error': 'Memory Limit Exceeded'}
#         elif result.returncode == 139 or 'segmentation fault' in stderr:
#             return {'error': 'Runtime Error'}
#         elif result.returncode != 0:
#             return {'error': 'Runtime Error', 'details': stderr}

#         output = output_path.read_text().strip()
#         return {'output': output}

#     except subprocess.TimeoutExpired:
#         return {'error': 'Time Limit Exceeded'}

#     finally:
#         delete_toggle = (
#             settings.DELETE_RUN_FILES_AFTER_EXECUTION if 'runs' in str(base_path) else
#             settings.DELETE_SUBMISSION_FILES_AFTER_EVALUATION
#         )
#         if delete_toggle:
#             shutil.rmtree(base_path, ignore_errors=True)

from pathlib import Path
import uuid
import subprocess
import shutil
import platform
from django.conf import settings

ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}

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

    system = platform.system()
    c_compiler = 'gcc' if system != 'Darwin' else 'clang'
    cpp_compiler = 'g++' if system != 'Darwin' else 'clang++'

    try:
        # --- Compilation ---
        if language in ['c', 'cpp']:
            exe_path = base_path / f"a_{uid}.out"
            compile_cmd = [c_compiler if language == 'c' else cpp_compiler, str(code_path), '-o', str(exe_path)]
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
            run_dir = None
            if language == 'python':
                run_cmd = ['python3' if system != 'Windows' else 'python', str(code_path)]
                full_cmd = run_cmd
            elif language in ['c', 'cpp']:
                run_cmd = [str(exe_path)]
                if system == 'Windows':
                    full_cmd = run_cmd
                else:
                    full_cmd = ['bash', '-c', f'ulimit -v {memory_limit * 1024}; timeout {time_limit} {" ".join(run_cmd)}']
            elif language == 'java':
                run_cmd = ['java', f'-Xmx{memory_limit}m', '-cp', str(code_dir), 'Main']
                run_dir = str(code_dir)
                full_cmd = run_cmd

            result = subprocess.run(
                full_cmd,
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                timeout=time_limit + 1,
                cwd=run_dir
            )

        stderr = result.stderr.decode().strip().lower()

        # --- Verdict checks ---
        if result.returncode == 124:
            return {'error': 'Time Limit Exceeded'}
        if result.returncode == 137 or 'killed' in stderr:
            return {'error': 'Memory Limit Exceeded'}
        if result.returncode == 139 or 'segmentation fault' in stderr:
            return {'error': 'Runtime Error'}
        if any(kw in stderr for kw in ['memoryerror', 'cannot allocate', 'outofmemory']):
            return {'error': 'Memory Limit Exceeded'}
        if result.returncode != 0:
            return {'error': 'Runtime Error', 'details': stderr}

        output = output_path.read_text().strip()
        return {'output': output}

    except subprocess.TimeoutExpired:
        return {'error': 'Time Limit Exceeded'}
    except Exception as e:
        return {'error': 'Unexpected Error', 'details': str(e)}
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

import markdown
import bleach
from django.utils.html import escape

@login_required
def problem_detail(request, code):
    problem = get_object_or_404(Problem, code=code)
    verdict = None

    # Optional: allow basic safe tags including <hr>, <strong>, etc.
    allowed_tags = [
        "p", "strong", "em", "ul", "ol", "li", "pre", "code",
        "br", "hr", "h1", "h2", "h3", "blockquote"
    ]

    # def render_md(content):
    #     return bleach.clean(
    #         markdown.markdown(content or "", extensions=["extra"]),
    #         tags=allowed_tags,
    #         strip=True
    #     )

    def render_md(content):
        if not content:
            return ''
        # Clean whitespace first
        content = content.strip()

        # Remove extra empty lines (e.g., double \n)
        content = re.sub(r'\n{2,}', '\n', content)

        rendered = markdown.markdown(content, extensions=["extra"])
        return bleach.clean(rendered, tags=allowed_tags, strip=True)



    # Render markdown into HTML
    problem.description = render_md(problem.description)
    problem.input_format = render_md(problem.input_format)
    problem.output_format = render_md(problem.output_format)
    problem.constraints = render_md(problem.constraints)
    # problem.sample_input = f"<pre>{escape(problem.sample_input.strip())}</pre>"
    # problem.sample_output = f"<pre>{escape(problem.sample_output.strip())}</pre>"
    problem.sample_input = render_md(problem.sample_input)
    problem.sample_output = render_md(problem.sample_output)


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

    return render(request, 'problem_detail.html', {
        'problem': problem,
        'verdict': verdict
    })


@csrf_exempt
@login_required
def run_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    code = request.POST.get('code', '')
    language = request.POST.get('language', '').lower()
    custom_input = request.POST.get('custom_input', '')
    time_limit = int(request.POST.get('time_limit', 1) or 1)
    memory_limit = int(request.POST.get('memory_limit', 128) or 128)

    uid = str(uuid.uuid4())
    base_path = Path(settings.BASE_DIR) / 'submission_files' / 'runs' / f"{language}_{uid}"

    result = run_code_util(code, language, custom_input, base_path,
                           time_limit=time_limit, memory_limit=memory_limit)
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



from .forms import ProblemForm, TestCaseFormSet  # make sure these are imported
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

@login_required
@staff_member_required
def add_problem_view(request):
    if request.method == "POST":
        problem_form = ProblemForm(request.POST)
        formset = TestCaseFormSet(request.POST)

        if problem_form.is_valid() and formset.is_valid():
            problem = problem_form.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    test_case = form.save(commit=False)
                    test_case.problem = problem
                    test_case.save()

            messages.success(request, "✅ Problem added successfully!")
            return redirect("add_problem")
        else:
            messages.error(request, "⚠️ Please fix the errors below.")
            print("Problem form errors:", problem_form.errors)
            print("Testcase formset errors:", [f.errors for f in formset])

    else:
        problem_form = ProblemForm()
        formset = TestCaseFormSet()

    return render(request, "add_problem.html", {
        "problem_form": problem_form,
        "formset": formset,
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


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Problem, TestCase
from .forms import ProblemForm, TestCaseForm

@staff_member_required
def update_problem_view(request, code):
    problem = get_object_or_404(Problem, code=code)

    TestCaseFormSet = inlineformset_factory(
        Problem,
        TestCase,
        form=TestCaseForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        formset = TestCaseFormSet(request.POST, instance=problem, prefix='testcases')

        form_valid = form.is_valid()
        formset_valid = formset.is_valid()

        if form_valid and formset_valid:
            form.save()

            test_cases = formset.save(commit=False)
            for tc in test_cases:
                tc.problem = problem
                tc.save()

            for obj in formset.deleted_objects:
                obj.delete()

            messages.success(request, "Problem updated successfully.")
            return redirect('manage_problems')

        else:
            messages.error(request, "⚠️ Please fix the errors below.")
            print("❌ Problem form errors:", form.errors)

            for f in formset.forms:
                # Avoid printing errors of deleted forms
                if f.cleaned_data.get('DELETE', False):
                    continue
                if f.errors:
                    print("❌ TestCase form errors:", f.errors)

    else:
        form = ProblemForm(instance=problem)
        formset = TestCaseFormSet(instance=problem, prefix='testcases')

    return render(request, 'update_problem.html', {
        'form': form,
        'formset': formset,
        'problem': problem,
    })


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_problems_view(request):
    problems = Problem.objects.all().order_by('id')
    return render(request, 'manage_problems.html', {'problems': problems})


from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Problem

@staff_member_required
def delete_problem_view(request, code):
    problem = get_object_or_404(Problem, code=code)
    if request.method == "POST":
        problem.delete()
        messages.success(request, f"🗑️ Problem '{code}' deleted successfully!")
        return redirect('manage_problems')
    else:
        messages.error(request, "❌ Invalid delete request.")
        return redirect('manage_problems')


@login_required
def online_compiler(request):
    return render(request, 'online_compiler.html')

@login_required
def ai_suggestions(request):
    # Placeholder for AI suggestions logic
    # This could be integrated with an AI model or API to provide code suggestions
    return render(request, 'ai_suggestions.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from judge.models import Submission
from judge.forms import EditProfileForm, CustomPasswordChangeForm


@login_required
def profile_view(request):
    user = request.user
    limit = request.GET.get('limit', '10')
    all_subs = Submission.objects.filter(user=user).order_by('-submitted_at')

    # ✅ Apply limit filter
    if limit != 'all':
        try:
            limit = int(limit)
            all_subs = all_subs[:limit]
        except ValueError:
            limit = 10
            all_subs = all_subs[:limit]

    # ✅ Stats calculation
    total = Submission.objects.filter(user=user).count()
    ac = Submission.objects.filter(user=user, verdict='Accepted').count()
    accuracy = (ac / total) * 100 if total > 0 else 0

    lang_counter = Submission.objects.filter(user=user).values('language', 'verdict').annotate(count=Count('id'))
    lang_stats = {}
    for entry in lang_counter:
        lang = entry['language']
        verdict = entry['verdict']
        count = entry['count']
        lang_stats.setdefault(lang, {})[verdict] = count

    # ✅ Always initialize both forms (whether POST or GET)
    profile_form = EditProfileForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user)

    # ✅ Handle POST forms
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = EditProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please fix the password form errors.')

    # ✅ Final context rendering
    return render(request, 'profile.html', {
        'submissions': all_subs,
        'stats': {
            'total': total,
            'ac': ac,
            'accuracy': accuracy,
            'lang_stats': lang_stats,
        },
        'profile_form': profile_form,
        'password_form': password_form,
    })


from .models import Contest, Problem, ContestSubmission
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def contest_list_view(request):
    now = timezone.now()
    upcoming = Contest.objects.filter(start_time__gt=now).order_by('start_time')
    ongoing = Contest.objects.filter(start_time__lte=now, end_time__gte=now).order_by('end_time')
    past = Contest.objects.filter(end_time__lt=now).order_by('-end_time')
    return render(request, 'contests/contest_list.html', {
        'upcoming': upcoming,
        'ongoing': ongoing,
        'past': past,
    })


def contest_detail_view(request, code):
    contest = get_object_or_404(Contest, code=code)
    problems = contest.problems.all()
    return render(request, 'contests/contest_detail.html', {
        'contest': contest,
        'problems': problems
    })


import re
import uuid
from pathlib import Path
from django.conf import settings

@login_required
def contest_problem_view(request, code, problem_code):
    contest = get_object_or_404(Contest, code=code)
    problem = get_object_or_404(Problem, code=problem_code)

    if not contest.is_active():
        return render(request, 'contests/contest_closed.html', {
            'contest': contest,
            'now' : timezone.now()
        })

    verdict = None

    if request.method == 'POST':
        code_submitted = request.POST.get('code')
        language = request.POST.get('language', '').lower()
        testcases = problem.testcases.all()

        uid = str(uuid.uuid4())
        base_path = Path(settings.BASE_DIR) / 'submission_files' / 'runs' / f"{language}_{uid}"

        for test in testcases:
            result = run_code_util(
                code_submitted,
                language,
                test.input,
                base_path,
                time_limit=problem.time_limit,
                memory_limit=problem.memory_limit
            )

            if 'error' in result:
                verdict = result['error']  # Could be CE, RTE, TLE, MLE, described above in the utility function.
                break

            normalized_output = re.sub(r'\s+', ' ', result['output'].strip())
            expected_output = re.sub(r'\s+', ' ', test.output.strip())
            if normalized_output != expected_output:
                verdict = 'Wrong Answer'
                break
        else:
            verdict = 'Accepted'

        # ✅ Save contest submission with verdict
        ContestSubmission.objects.create(
            user=request.user,
            contest=contest,
            problem=problem,
            code=code_submitted,
            language=language,
            verdict=verdict
        )

    return render(request, 'contests/contest_problem.html', {
        'contest': contest,
        'problem': problem,
        'verdict': verdict
    })


from .forms import ContestForm  

@login_required
@staff_member_required
def add_contest_view(request):
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)  # Don't commit yet!
            contest.created_by = request.user  # Set the missing field
            contest.save()                     # Now save safely
            form.save_m2m()                    # For the ManyToManyField: problems
            return redirect('contest_list')    # Your contest listing page
    else:
        form = ContestForm()
    return render(request, 'contests/add_contest.html', {'form': form})





