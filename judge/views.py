from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission

from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

import re
import uuid 
import os
from django.conf import settings
import subprocess
import shutil



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
        language = request.POST.get('language', '').lower()
        user = request.user
        testcases = problem.testcases.all()

        if not testcases.exists():
            return HttpResponse("No test cases available for this problem.", status=400)

        uid = str(uuid.uuid4())[:8]
        base_path = os.path.join(settings.BASE_DIR, 'submission_files', 'submissions', f"{language}_{uid}")
        os.makedirs(base_path, exist_ok=True)

        ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}
        if language not in ext_map:
            return HttpResponse("Unsupported language", status=400)

        filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
        code_path = os.path.join(base_path, filename)
        input_path = os.path.join(base_path, f"input_{uid}.txt")

        with open(code_path, 'w') as f:
            f.write(submitted_code)

        verdict = 'Accepted'
        output_paths = []

        for tc in testcases:
            output_path = os.path.join(base_path, f"output_{uid}_{tc.id}.txt")
            output_paths.append(output_path)

            with open(input_path, 'w') as f:
                f.write(tc.input)

            try:
                # Compilation step
                if language in ['c', 'cpp']:
                    exe_path = os.path.join(base_path, f"a_{uid}.out")
                    compile_cmd = ['gcc', code_path, '-o', exe_path] if language == 'c' else ['g++', code_path, '-o', exe_path]
                    result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        verdict = 'Compilation Error'
                        break

                elif language == 'java':
                    compile_cmd = ['javac', '-d', base_path, code_path]
                    result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0 or not os.path.exists(os.path.join(base_path, 'Main.class')):
                        verdict = 'Compilation Error'
                        break

                elif language == 'python':
                    try:
                        compile(submitted_code, filename, 'exec')
                    except SyntaxError:
                        verdict = 'Compilation Error'
                        break

                # Execution step
                with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
                    if language == 'python':
                        run_cmd = ['python3', code_path]
                        run_dir = None
                    elif language in ['c', 'cpp']:
                        run_cmd = [exe_path]
                        run_dir = None
                    elif language == 'java':
                        run_cmd = ['java', '-Xmx128m', '-cp', base_path, 'Main']
                        run_dir = base_path

                    run_cmd_str = (
                        " ".join(run_cmd) if language == 'java'
                        else f'ulimit -v 131072; {" ".join(run_cmd)}'
                    )

                    result = subprocess.run(
                        run_cmd_str, stdin=infile, stdout=outfile, stderr=subprocess.PIPE,
                        timeout=1, cwd=run_dir, shell=True
                    )

                # Check for runtime or memory issues
                code = result.returncode
                stderr = result.stderr.decode().strip().lower()

                if code == 137 or 'outofmemoryerror' in stderr or 'killed' in stderr:
                    verdict = 'Memory Limit Exceeded'
                    break
                elif code == 139 or 'segmentation fault' in stderr:
                    verdict = 'Runtime Error'
                    break
                elif code != 0:
                    verdict = 'Runtime Error'
                    break

                # Output comparison
                with open(output_path) as f:
                    user_output = re.sub(r'\s+', ' ', f.read().strip())
                expected_output = re.sub(r'\s+', ' ', tc.output.strip())

                if user_output != expected_output:
                    verdict = 'Wrong Answer'
                    break

            except subprocess.TimeoutExpired:
                verdict = 'Time Limit Exceeded'
                break

        # Save submission
        submission = Submission.objects.create(
            user=user, problem=problem, code=submitted_code,
            language=language, verdict=verdict
        )

        # Clean up
        if getattr(settings, 'DELETE_SUBMISSION_FILES_AFTER_EVALUATION', True):
            for path in [code_path, input_path] + output_paths:
                if os.path.exists(path): os.remove(path)
            if language in ['c', 'cpp'] and 'exe_path' in locals():
                os.remove(exe_path)
            if language == 'java':
                class_file = os.path.join(base_path, 'Main.class')
                if os.path.exists(class_file): os.remove(class_file)
            shutil.rmtree(base_path, ignore_errors=True)

        return redirect('submission_detail', id=submission.id)

    return render(request, 'problem_detail.html', {'problem': problem, 'verdict': verdict})

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
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('problem_list')
        
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



@login_required
def submission_detail(request, id):
    submission = get_object_or_404(Submission, id=id)
    
    return render(request, 'submission_detail.html', {
        'submission': submission,
    })



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import shutil

@csrf_exempt
@login_required
def run_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    code = request.POST.get('code', '')
    language = request.POST.get('language', '').lower()
    custom_input = request.POST.get('custom_input', '')

    uid = str(uuid.uuid4())[:8]
    base_path = os.path.join(settings.BASE_DIR, 'submission_files', 'runs', f"{language}_{uid}")
    os.makedirs(base_path, exist_ok=True)

    ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}
    if language not in ext_map:
        return JsonResponse({'error': 'Unsupported language'}, status=400)

    filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
    code_path = os.path.join(base_path, filename)
    input_path = os.path.join(base_path, f"input_{uid}.txt")
    output_path = os.path.join(base_path, f"output_{uid}.txt")

    with open(code_path, 'w') as f: f.write(code)
    with open(input_path, 'w') as f: f.write(custom_input)

    try:
        # Compilation
        if language in ['c', 'cpp']:
            exe_path = os.path.join(base_path, f"a_{uid}.out")
            compile_cmd = ['gcc', code_path, '-o', exe_path] if language == 'c' else ['g++', code_path, '-o', exe_path]
            result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                return JsonResponse({'error': 'Compilation Error', 'details': result.stderr.decode()})

        elif language == 'java':
            compile_cmd = ['javac', '-d', base_path, code_path]
            result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                return JsonResponse({'error': 'Compilation Error', 'details': result.stderr.decode()})

        elif language == 'python':
            try:
                compile(code, filename, 'exec')
            except SyntaxError as e:
                return JsonResponse({'error': 'Compilation Error', 'details': str(e)})

        # Execution
        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            if language == 'python':
                run_cmd = ['python3', code_path]
                run_dir = None
            elif language in ['c', 'cpp']:
                run_cmd = [exe_path]
                run_dir = None
            elif language == 'java':
                run_cmd = ['java', '-Xmx128m', '-cp', base_path, 'Main']
                run_dir = base_path

            run_cmd_str = (
                " ".join(run_cmd) if language == 'java'
                else f'ulimit -v 131072; {" ".join(run_cmd)}'
            )

            result = subprocess.run(
                run_cmd_str, stdin=infile, stdout=outfile,
                stderr=subprocess.PIPE, timeout=1, cwd=run_dir, shell=True
            )

        return_code = result.returncode
        stderr = result.stderr.decode().strip()

        if return_code != 0:
            return JsonResponse({'error': 'Runtime Error', 'details': stderr})

        with open(output_path, 'r') as f:
            output = f.read().strip()

        return JsonResponse({'output': output})

    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Time Limit Exceeded'})

    finally:
        shutil.rmtree(base_path, ignore_errors=True)
        if language in ['c', 'cpp'] and 'exe_path' in locals():
            os.remove(exe_path)
        if language == 'java':
            class_file = os.path.join(base_path, 'Main.class')
            if os.path.exists(class_file): os.remove(class_file)


    

