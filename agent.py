# agent.py (Versi 4)

import google.generativeai as genai

def choose_tool(file_name: str, user_prompt: str) -> str:
    """Menggunakan Gemini untuk memilih alat yang tepat."""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        system_prompt = f"""
        Anda adalah CodeGuardian, seorang agent ahli yang bertugas memilih alat yang tepat.
        Berdasarkan nama file '{file_name}' dan permintaan pengguna '{user_prompt}', tentukan alat mana yang paling sesuai dari pilihan berikut:
        - 'analyze_code': Jika file adalah source code (.py, .js).
        - 'parse_log': Jika file adalah file log (.log, .txt).
        - 'inspect_dependencies': Jika file adalah 'requirements.txt'.
        - 'general_qna': Untuk pertanyaan umum lainnya.

        Balas HANYA dengan nama alat yang dipilih. Contoh: analyze_code
        """
        response = model.generate_content(system_prompt)
        tool_name = response.text.strip().lower()
        return tool_name
    except Exception as e:
        # Jika gagal memilih alat, kembalikan 'error' sebagai nama alat
        print(f"Error di choose_tool: {e}") # Untuk debugging di konsol
        return "error_api"