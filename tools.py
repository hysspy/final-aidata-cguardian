# tools.py (Versi 4)

import re
from collections import Counter

def analyze_code(file_content: str) -> dict:
    """Menganalisis konten file kode Python."""
    try:
        lines = file_content.splitlines()
        total_lines = len(lines)
        functions = re.findall(r"def\s+(\w+)\s*\(", file_content)
        function_count = len(functions)
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        return {
            "status": "sukses",
            "total_lines": total_lines,
            "function_count": function_count,
            "function_names": functions,
            "comment_lines": comment_lines
        }
    except Exception as e:
        return {"status": "error", "message": f"Gagal menganalisis kode: {e}"}

def parse_log(file_content: str) -> dict:
    """Mem-parsing konten file log."""
    try:
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
            "status": "sukses",
            "total_lines": len(lines),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "most_common_error_summary": error_summary
        }
    except Exception as e:
        return {"status": "error", "message": f"Gagal mem-parsing log: {e}"}

def inspect_dependencies(file_content: str) -> dict:
    """Memeriksa file requirements.txt."""
    try:
        dependencies = [line.strip() for line in file_content.splitlines() if line.strip() and not line.startswith('#')]
        return {
            "status": "sukses",
            "dependency_count": len(dependencies),
            "dependencies": dependencies
        }
    except Exception as e:
        return {"status": "error", "message": f"Gagal memeriksa dependensi: {e}"}