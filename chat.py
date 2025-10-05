# chat.py (Versi 4)

import google.generativeai as genai

def initialize_chat(api_key: str):
    """Mengonfigurasi API dan menginisialisasi sesi chat."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        # Kembalikan error agar bisa ditampilkan di UI
        return f"Error Inisialisasi: {e}"

def send_chat_message(chat_session, prompt: str) -> str:
    """Mengirim pesan ke sesi chat dan mengembalikan respons."""
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error saat mengirim pesan ke API: {e}"