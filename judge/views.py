from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from problems.models import Problem, TestCase
from judge.models import Submission, ContestSubmission
from .forms import RegisterForm
from problems.views import run_code_util



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
from django.contrib.admin.views.decorators import staff_member_required

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





