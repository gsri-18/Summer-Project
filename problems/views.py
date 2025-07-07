from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings


from pathlib import Path
import re
import uuid


from .models import Problem
from judge.models import Submission
from core.utils.code_executor import run_code_util


# Create your views here.

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problems.html', {'problems': problems})

import markdown
import bleach

@login_required
def problem_detail(request, code):
    problem = get_object_or_404(Problem, code=code)
    verdict = None

    # Optional: allow basic safe tags including <hr>, <strong>, etc.
    allowed_tags = [
        "p", "strong", "em", "ul", "ol", "li", "pre", "code",
        "br", "hr", "h1", "h2", "h3", "blockquote"
    ]


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
                memory_limit=problem.memory_limit,
                use_docker=problem.use_docker,
            )

            if 'error' in result:
                verdict = result['error']
                break

            normalized_output = re.sub(r'\s+', ' ', result['output'].strip())
            expected_output = re.sub(r'\s+', ' ', tc.output.strip())
            if normalized_output != expected_output:
                verdict = 'Wrong Answer'
                break

        # Construct path: BASE_DIR/submission_files/submissions/user_<id>/submission_<uuid>/
        user_id = request.user.id
        submission_uid = str(uuid.uuid4())
        code_dir = Path(settings.BASE_DIR) / 'submission_files' / 'submissions' / f'user_{user_id}' / f'sub_{submission_uid}'
        code_dir.mkdir(parents=True, exist_ok=True)

        # Determine file extension
        ext_map = {'python': '.py', 'cpp': '.cpp', 'c': '.c', 'java': '.java'}
        file_ext = ext_map.get(language, '.txt')
        filename = f"solution{file_ext}"
        code_file_path = code_dir / filename
        code_file_path.write_text(submitted_code)

        # Save to DB with path
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=submitted_code,
            language=language,
            verdict=verdict,
            code_file_path=str(code_file_path.relative_to(settings.BASE_DIR))  # Make it project-relative
        )

        return redirect('submission_detail', id=submission.id)

    return render(request, 'problems/problem_detail.html', {
        'problem': problem,
        'verdict': verdict
    })

# compiler/views.py or problems/views.py or wherever
from core.utils.code_runner import handle_run_code_view_logic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def run_code_view(request):
    result, status = handle_run_code_view_logic(request)
    return JsonResponse(result, status=status)



from judge.forms import ProblemForm, TestCaseFormSet  # make sure these are imported
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

    return render(request, "problems/add_problem.html", {
        "problem_form": problem_form,
        "formset": formset,
    })


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Problem, TestCase
from judge.forms import ProblemForm, TestCaseForm

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

    return render(request, 'problems/update_problem.html', {
        'form': form,
        'formset': formset,
        'problem': problem,
    })


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_problems_view(request):
    problems = Problem.objects.all().order_by('id')
    return render(request, 'problems/manage_problems.html', {'problems': problems})


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
    
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai

@csrf_exempt
def ai_assist_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    data = json.loads(request.body)
    action = data.get('action')
    prompt = data.get('prompt')
    code = data.get('code', '')

    if not prompt:
        return JsonResponse({'error': 'Prompt missing'}, status=400)

    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return JsonResponse({'result': response.text})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


