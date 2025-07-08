from django.conf import settings
from pathlib import Path
import platform
import uuid
import subprocess
import shutil


ext_map = {'python': '.py', 'c': '.c', 'cpp': '.cpp', 'java': '.java'}

def run_code_util(code, language, input_data, base_path,
                  time_limit=1, memory_limit=128, use_docker=False):
    
    if use_docker:
        return run_in_docker(code, language, input_data, time_limit, memory_limit, base_path)


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
            settings.DELETE_RUN_FILES_AFTER_EXECUTION if 'runs' in base_path.parts else
            settings.DELETE_SUBMISSION_FILES_AFTER_EVALUATION
        )
        if delete_toggle:
            shutil.rmtree(base_path, ignore_errors=True)



def run_in_docker(code, language, input_data, time_limit, memory_limit, base_dir):

    uid = str(uuid.uuid4())
    # base_dir = Path(settings.BASE_DIR) / "submission_files" / "docker_temp" / uid
    base_dir.mkdir(parents=True, exist_ok=True)

    ext_map = {'python': '.py', 'cpp': '.cpp', 'c': '.c', 'java': '.java'}
    file_ext = ext_map.get(language)
    if not file_ext:
        return {'error': 'Unsupported language'}

    filename = 'Main.java' if language == 'java' else f'code_{uid}{file_ext}'
    code_file = base_dir / filename
    input_file = base_dir / "input.txt"
    output_file = base_dir / "output.txt"

    time_limit = time_limit + 1  # Add a buffer to the time limit for Docker execution

    code_file.write_text(code)
    input_file.write_text(input_data)
    print("🐳 [Docker] Mount base_dir:", base_dir)
    print("📝 Writing code to:", code_file)
    print("📝 Writing input to:", input_file)
    print("✅ Code file exists?", code_file.exists())
    print("✅ Input file exists?", input_file.exists())


    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{base_dir}:/runner",
        "--cpus", "1.0",
        "--network", "none",
        "codeverse-runner",
        "/scripts/run_code.sh",
        language,                      # $1 -> LANG
        f"/runner/{code_file.name}",   # $2 -> CODE_FILE
        f"/runner/{input_file.name}",  # $3 -> INPUT_FILE
        f"/runner/{output_file.name}", # $4 -> OUTPUT_FILE
        str(time_limit),               # $5 -> TIME_LIMIT
        str(memory_limit)              # $6 -> MEMORY_LIMIT ✅ (was missing!)
    ]


    try:
        result = subprocess.run(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=time_limit + 3
        )

        if result.returncode != 0:
            return {
                'error': 'Runtime Error',
                'details': result.stderr.decode().strip()
            }

        output = output_file.read_text().strip()

        print("📤 Docker output:", output_file.read_text().strip() if output_file.exists() else "⚠️ Output file missing")


        return {'output': output}

    except subprocess.TimeoutExpired:
        return {'error': 'Time Limit Exceeded'}
    except Exception as e:
        return {'error': 'Unexpected Error', 'details': str(e)}
    finally:
        delete_toggle = (
            settings.DELETE_RUN_FILES_AFTER_EXECUTION if 'runs' in base_dir.parts else
            settings.DELETE_SUBMISSION_FILES_AFTER_EVALUATION
        )
        if delete_toggle:
            shutil.rmtree(base_dir, ignore_errors=True)
            print("🗑️ Docker temp files deleted:", base_dir)
        pass

