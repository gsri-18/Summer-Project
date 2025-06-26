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

        # Generate unique filenames
        uid = str(uuid.uuid4())[:8]
        base_path = os.path.join(settings.BASE_DIR, 'submission_files')

        ext_map = {
            'python': '.py',
            'c': '.c',
            'cpp': '.cpp',
            'java': '.java',
        }

        if language not in ext_map:
            return HttpResponse("Unsupported language", status=400)

        filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
        code_path = os.path.join(base_path, filename)
        input_path = os.path.join(base_path, f"input_{uid}.txt")


        # Save submitted code
        with open(code_path, 'w') as f:
            f.write(submitted_code)

        print("✅ Written code to:", code_path)
        print("🔍 Code content:\n", submitted_code)

        verdict = 'Accepted'
        output_paths = []

        for tc in testcases:

            # Generate unique output file path for each test case
            output_path = os.path.join(base_path, f"output_{uid}_{tc.id}.txt")

            output_paths.append(output_path)


            # Save test input
            with open(input_path, 'w') as f:
                f.write(tc.input)

            try:
                # 🧠 Compile C/C++/Java
                if language in ['c', 'cpp']:
                    exe_path = os.path.join(base_path, f'a_{uid}.out')
                    compile_cmd = ['gcc', code_path, '-o', exe_path] if language == 'c' else ['g++', code_path, '-o', exe_path]
                    compile_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if compile_result.returncode != 0:
                        print("❌ Compilation Error:", compile_result.stderr.decode().strip())
                        verdict = 'Compilation Error'
                        break

                elif language == 'java':
                    compile_cmd = ['javac', '-d', base_path, code_path]
                    compile_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    if compile_result.returncode != 0:
                        print("❌ Compilation Error:", compile_result.stderr.decode().strip())
                        verdict = 'Compilation Error'
                        break

                    # Optional: Check if Main.class exists
                    if not os.path.exists(os.path.join(base_path, 'Main.class')):
                        print("⚠️ Main.class not found after javac!")
                        verdict = 'Runtime Error'
                        break

                # 🧠 Run the code
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

                    if language == 'python':
                        # Try compiling first (syntax check only)
                        try:
                            compile(submitted_code, filename, 'exec')
                        except SyntaxError as e:
                            print("❌ Python Syntax Error:", e)
                            verdict = 'Compilation Error'
                            break


                    # ulimit and command construction
                    if language == 'java':
                        # Java: Use Xmx, no ulimit
                        run_cmd_str = " ".join(run_cmd)
                    else:
                        # C/C++/Python: Use ulimit
                        run_cmd_str = f'ulimit -v 131072; {" ".join(run_cmd)}'  # 128MB

                    run_result = subprocess.run(
                        run_cmd_str,
                        stdin=infile,
                        stdout=outfile,
                        stderr=subprocess.PIPE,
                        timeout=1,
                        cwd=run_dir,
                        shell=True
                    )


                    return_code = run_result.returncode
                    stderr_output = run_result.stderr.decode().strip().lower()

                    print("⛔ Exit code:", return_code)
                    print("⛔ Stderr output:", stderr_output)

                    if (
                        return_code == 137 or 
                        'killed' in stderr_output or 
                        'memoryerror' in stderr_output or 
                        'outofmemoryerror' in stderr_output
                    ):
                        verdict = 'Memory Limit Exceeded'

                        break
                    elif return_code == 139 or 'segmentation fault' in stderr_output or 'core dumped' in stderr_output:
                        verdict = 'Runtime Error'
                        break
                    elif return_code != 0:
                        verdict = 'Runtime Error'
                        break



                # 🧠 Compare output
                with open(output_path, 'r') as f:
                    user_output = f.read().strip()
                expected_output = tc.output.strip()

                def normalize_output(output):
                    return re.sub(r'\s+', ' ', output.strip())

                print("📥 Input Given:\n", repr(tc.input))
                print("🎯 Expected Output:\n", repr(expected_output))
                print("💡 User Output:\n", repr(user_output))

                if normalize_output(user_output) != normalize_output(expected_output):
                    print("❌ WRONG ANSWER CHECK:")
                    print("Expected:", repr(normalize_output(expected_output)))
                    print("Got     :", repr(normalize_output(user_output)))
                    verdict = 'Wrong Answer'
                    break

            except subprocess.TimeoutExpired:
                verdict = 'Time Limit Exceeded'
                break

        # ✅ Save submission to DB
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=submitted_code,
            language=language,
            verdict=verdict,
        )

        # Clean up only if enabled
        if getattr(settings, 'DELETE_SUBMISSION_FILES_AFTER_EVALUATION', True):
            for path in [code_path, input_path] + output_paths:
                if os.path.exists(path):
                    os.remove(path)

            if language in ['c', 'cpp'] and 'exe_path' in locals() and os.path.exists(exe_path):
                os.remove(exe_path)

            if language == 'java':
                class_file = os.path.join(base_path, 'Main.class')
                if os.path.exists(class_file):
                    os.remove(class_file)


        return redirect('submission_detail', id=submission.id)

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

@csrf_exempt
@login_required
def run_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    code = request.POST.get('code', '')
    language = request.POST.get('language', '').lower()
    custom_input = request.POST.get('custom_input', '')

    uid = str(uuid.uuid4())[:8]
    base_path = os.path.join(settings.BASE_DIR, 'submission_files')

    ext_map = {
        'python': '.py',
        'c': '.c',
        'cpp': '.cpp',
        'java': '.java',
    }

    if language not in ext_map:
        return JsonResponse({'error': 'Unsupported language'}, status=400)

    filename = 'Main.java' if language == 'java' else f"code_{uid}{ext_map[language]}"
    code_path = os.path.join(base_path, filename)
    input_path = os.path.join(base_path, f"input_{uid}.txt")
    output_path = os.path.join(base_path, f"output_{uid}.txt")

    with open(code_path, 'w') as f:
        f.write(code)

    with open(input_path, 'w') as f:
        f.write(custom_input)

    try:
        # Compile
        if language in ['c', 'cpp']:
            exe_path = os.path.join(base_path, f'a_{uid}.out')
            compile_cmd = ['gcc', code_path, '-o', exe_path] if language == 'c' else ['g++', code_path, '-o', exe_path]
            compile_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if compile_result.returncode != 0:
                return JsonResponse({'error': 'Compilation Error', 'details': compile_result.stderr.decode()})

        elif language == 'java':
            compile_cmd = ['javac', '-d', base_path, code_path]
            compile_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if compile_result.returncode != 0:
                return JsonResponse({'error': 'Compilation Error', 'details': compile_result.stderr.decode()})

        elif language == 'python':
            try:
                compile(code, filename, 'exec')  # Syntax check
            except SyntaxError as e:
                return JsonResponse({'error': 'Compilation Error', 'details': str(e)})

        # Run
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
                " ".join(run_cmd)
                if language == 'java'
                else f'ulimit -v 131072; {" ".join(run_cmd)}'
            )

            run_result = subprocess.run(
                run_cmd_str,
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                timeout=1,
                cwd=run_dir,
                shell=True
            )

        # Read output
        with open(output_path, 'r') as f:
            output = f.read().strip()

        return_code = run_result.returncode
        stderr = run_result.stderr.decode().strip()

        if return_code != 0:
            return JsonResponse({'error': 'Runtime Error', 'details': stderr})

        return JsonResponse({'output': output})

    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Time Limit Exceeded'})
    

    finally:
        #  Cleanup files
        for path in [code_path, input_path, output_path]:
            if os.path.exists(path):
                os.remove(path)

        # Remove compiled files
        if language in ['c', 'cpp'] and 'exe_path' in locals() and os.path.exists(exe_path):
            os.remove(exe_path)

        if language == 'java':
            class_file = os.path.join(base_path, 'Main.class')
            if os.path.exists(class_file):
                os.remove(class_file)



    

