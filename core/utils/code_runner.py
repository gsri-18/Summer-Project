# core/utils/code_runner.py
import uuid
from pathlib import Path
from django.conf import settings
from core.utils.code_executor import run_code_util

def handle_run_code_view_logic(request):
    if request.method != 'POST':
        return {'error': 'Only POST allowed'}, 405

    code = request.POST.get('code', '')
    language = request.POST.get('language', '').lower()
    custom_input = request.POST.get('custom_input', '')
    time_limit = int(request.POST.get('time_limit', 1) or 1)
    memory_limit = int(request.POST.get('memory_limit', 128) or 128)

    uid = str(uuid.uuid4())
    base_path = Path(settings.BASE_DIR) / 'submission_files' / 'runs' / f"{language}_{uid}"

    result = run_code_util(
        code=code,
        language=language,
        input_data=custom_input,
        base_path=base_path,
        time_limit=time_limit,
        memory_limit=memory_limit
    )

    return result, 200
