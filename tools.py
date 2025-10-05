# tools.py

import re
from collections import Counter

def analyze_code(file_content: str) -> dict:
    # ... (kode sama seperti sebelumnya)
    lines = file_content.splitlines()
    total_lines = len(lines)
    functions = re.findall(r"def\s+(\w+)\s*\(", file_content)
    function_count = len(functions)
    comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
    return {
        "total_lines": total_lines,
        "function_count": function_count,
        "function_names": functions,
        "comment_lines": comment_lines
    }

def parse_log(file_content: str) -> dict:
    # ... (kode sama seperti sebelumnya)
    lines = file_content.splitlines()
    errors = [line for line in lines if "ERROR" in line.upper()]
    warnings = [line for line in lines if "WARNING" in line.upper()]
    error_summary = "Tidak ada error spesifik yang ditemukan."
    if errors:
        error_messages = [line.split('ERROR', 1)[-1].strip() for line in errors]
        most_common_error = Counter(error_messages).most_common(1)
        if most_common_error:
            error_summary = most_common_error[0][0]
    return {
        "total_lines": len(lines),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "most_common_error_summary": error_summary
    }

def inspect_dependencies(file_content: str) -> dict:
    # ... (kode sama seperti sebelumnya)
    dependencies = [line.strip() for line in file_content.splitlines() if line.strip() and not line.startswith('#')]
    return {
        "dependency_count": len(dependencies),
        "dependencies": dependencies
    }