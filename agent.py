# agent.py

import google.generativeai as genai

def choose_tool(file_name: str, user_prompt: str) -> str:
    # ... (kode sama seperti sebelumnya)
    model = genai.GenerativeModel('gemini-1.5-flash')
    system_prompt = f"""
    Anda adalah CodeGuardian, seorang agent ahli yang bertugas memilih alat yang tepat.
    Berdasarkan nama file '{file_name}' dan permintaan pengguna '{user_prompt}', tentukan alat mana yang paling sesuai dari pilihan berikut:
    - 'analyze_code': Jika file adalah source code (.py, .js) dan pengguna ingin tahu tentang struktur atau isi kode.
    - 'parse_log': Jika file adalah file log (.log, .txt) dan pengguna bertanya tentang error atau aktivitas.
    - 'inspect_dependencies': Jika file adalah 'requirements.txt' dan pengguna bertanya tentang library.
    - 'general_qna': Untuk pertanyaan umum atau jika jenis file tidak cocok dengan alat lain.

    Balas HANYA dengan nama alat yang dipilih. Contoh: analyze_code
    """
    response = model.generate_content(system_prompt)
    tool_name = response.text.strip().lower()
    return tool_name