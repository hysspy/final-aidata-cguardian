# app.py (Versi 4)

import streamlit as st
from tools import analyze_code, parse_log, inspect_dependencies
from agent import choose_tool
from chat import initialize_chat, send_chat_message

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="CodeGuardian Final", page_icon="🛡️", layout="wide")
st.title("🛡️ CodeGuardian: Agent Analisis Cerdas")
st.write("Analisis kode, log, atau error dengan mengunggah file atau paste konten langsung.")

# --- UI Sidebar ---
with st.sidebar:
    st.header("⚙️ Setting | 🛡️ CodeGuardian")
    if "GOOGLE_API_KEY" not in st.session_state:
        api_key_input = st.text_input("Masukkan Gemini API Key:", type="password", key="api_key_form")
        if st.button("Simpan API Key"):
            if api_key_input:
                st.session_state.GOOGLE_API_KEY = api_key_input
                st.rerun()
            else:
                st.warning("Mohon masukkan API Key.")
    else:
        st.success("API Key tersimpan.", icon="✔️")
    
    if st.button("Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.session_state.context_data = None
        st.session_state.context_name = None
        if 'chat' in st.session_state: del st.session_state['chat']
        st.rerun()

    st.header("📄 Sumber Konteks")
    input_method = st.radio("Metode input:", ("Upload File", "Paste Teks"))
    context_data, context_name = None, None
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Pilih file", type=['py', 'log', 'txt'])
        if uploaded_file:
            context_data = uploaded_file.getvalue().decode("utf-8")
            context_name = uploaded_file.name
    else:
        pasted_text = st.text_area("Paste konten:", height=250)
        if pasted_text:
            context_data = pasted_text
            context_name = "Teks yang di-paste"
    
    if context_data:
        st.session_state.context_data = context_data
        st.session_state.context_name = context_name

    # --- Peningkatan UX: Analisis Proaktif ---
    if "context_name" in st.session_state and st.session_state.context_name:
        st.success(f"Konteks aktif: **{st.session_state.context_name}**")
        if st.button("Beri Ringkasan Otomatis", use_container_width=True):
            st.session_state.run_auto_summary = True # Flag untuk dijalankan di alur utama

# --- Logika Utama Aplikasi ---
if "GOOGLE_API_KEY" not in st.session_state:
    st.info("Selamat datang! Mohon masukkan Gemini API Key di sidebar untuk memulai.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "chat" not in st.session_state:
    chat_session = initialize_chat(st.session_state.GOOGLE_API_KEY)
    # --- Peningkatan: Cek validitas API Key ---
    if isinstance(chat_session, str): # Jika initialize_chat mengembalikan string error
        st.error(f"Gagal menginisialisasi chat: {chat_session}")
        del st.session_state.GOOGLE_API_KEY # Hapus key yang salah
        st.stop()
    st.session_state.chat = chat_session

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Cek apakah ringkasan otomatis diminta
if st.session_state.get("run_auto_summary", False):
    prompt = "Berikan saya ringkasan umum dari konten yang diberikan."
    st.session_state.run_auto_summary = False # Reset flag
    # Baris ini diubah: Kita tidak perlu mengisi value, cukup nonaktifkan saja
    # untuk mencegah input ganda saat ringkasan otomatis berjalan.
    st.chat_input("Ringkasan otomatis sedang diproses...", disabled=True) 
else:
    prompt = st.chat_input("Tanya tentang konteks yang diberikan...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    if "context_data" not in st.session_state or not st.session_state.context_data:
        st.warning("Mohon sediakan konteks (upload/paste) terlebih dahulu.", icon="⚠️")
        st.stop()
    
    with st.chat_message("assistant"):
        with st.spinner("CodeGuardian sedang berpikir..."):
            # --- Peningkatan: Bungkus dengan try-except ---
            try:
                tool_name = choose_tool(st.session_state.context_name, prompt)
                
                if tool_name == "error_api":
                    response_text = "Maaf, terjadi masalah saat menghubungi API Gemini untuk memilih alat. Coba lagi nanti."
                else:
                    analysis_result = {}
                    if tool_name == 'analyze_code':
                        analysis_result = analyze_code(st.session_state.context_data)
                    elif tool_name == 'parse_log':
                        analysis_result = parse_log(st.session_state.context_data)
                    elif tool_name == 'inspect_dependencies':
                        analysis_result = inspect_dependencies(st.session_state.context_data)

                    # Cek jika tool menghasilkan error
                    if analysis_result.get("status") == "error":
                        response_text = f"Terjadi kesalahan pada alat analisis: {analysis_result.get('message')}"
                    else:
                        final_prompt = f"""KONTEKS ANALISIS:
- Nama Konteks: {st.session_state.context_name}
- Alat yang digunakan: {tool_name}
- Hasil Analisis Alat: {analysis_result or "Tidak ada analisis spesifik yang dijalankan."}
PERMINTAAN PENGGUNA: "{prompt}"
Tolong berikan jawaban yang komprehensif."""
                        response_text = send_chat_message(st.session_state.chat, final_prompt)
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_message = f"Terjadi error yang tidak terduga: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})