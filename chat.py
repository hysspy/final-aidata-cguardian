# chat.py

import google.generativeai as genai

def initialize_chat(api_key: str):
    """
    Mengonfigurasi API dan menginisialisasi model Generative AI untuk sesi chat.
    
    Args:
        api_key: Kunci API Google Gemini.
        
    Returns:
        Objek ChatSession atau None jika terjadi error.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])
        return chat
    except Exception as e:
        print(f"Error initializing chat model: {e}")
        return None

def send_chat_message(chat_session, prompt: str) -> str:
    """
    Mengirim pesan ke sesi chat dan mengembalikan respons teks.
    
    Args:
        chat_session: Objek ChatSession yang aktif.
        prompt: Prompt yang akan dikirim ke model.
        
    Returns:
        Teks respons dari model.
    """
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Maaf, terjadi error saat berkomunikasi dengan AI: {e}"