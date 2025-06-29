from django.conf import settings
from pathlib import Path
import platform
import uuid
import subprocess
import shutil


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