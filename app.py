# app.py

import streamlit as st
from tools import analyze_code, parse_log, inspect_dependencies
from agent import choose_tool
from chat import initialize_chat, send_chat_message

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="CodeGuardian v4",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CodeGuardian v4: Agent Analisis Cerdas")
st.write("Chatbot AI Agent untuk menganalisis kode, file log, dan dependensi proyek perangkat lunak")

# --- UI Sidebar ---
with st.sidebar:
    st.header("Pengaturan")
    if "GOOGLE_API_KEY" not in st.session_state:
        api_key_input = st.text_input("Masukkan Gemini API Key Anda:", type="password", key="api_key_form")
        if st.button("Simpan API Key"):
            if api_key_input:
                st.session_state.GOOGLE_API_KEY = api_key_input
                st.rerun()
            else:
                st.warning("Mohon masukkan API Key Anda.")
    else:
        st.success("API Key sudah tersimpan.", icon="✔️")

    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.session_state.context_data = None
        st.session_state.context_name = None
        if 'chat' in st.session_state: del st.session_state['chat']
        st.rerun()

    st.header("Sumber Konteks")
    # ... (kode UI untuk upload file dan paste teks sama seperti sebelumnya)
    input_method = st.radio("Pilih metode input:", ("Upload File", "Paste Teks"))
    context_data, context_name = None, None
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Pilih file", type=['py', 'log', 'txt'])
        if uploaded_file:
            context_data = uploaded_file.getvalue().decode("utf-8")
            context_name = uploaded_file.name
    else:
        pasted_text = st.text_area("Paste konten di sini:", height=250)
        if pasted_text:
            context_data = pasted_text
            context_name = "Teks yang di-paste"
    if context_data:
        st.session_state.context_data = context_data
        st.session_state.context_name = context_name
    if "context_name" in st.session_state and st.session_state.context_name:
        st.success(f"Konteks aktif: **{st.session_state.context_name}**")


# --- Logika Utama Aplikasi ---
if "GOOGLE_API_KEY" not in st.session_state:
    st.info("Selamat datang! Mohon masukkan Gemini API Key Anda di sidebar untuk memulai.")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = initialize_chat(st.session_state.GOOGLE_API_KEY)

if not st.session_state.chat:
    st.error("Gagal memulai sesi chat. Periksa kembali API Key Anda.")
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya tentang kode, log, atau error Anda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    if "context_data" not in st.session_state or not st.session_state.context_data:
        st.warning("Mohon unggah file atau paste teks terlebih dahulu.", icon="⚠️")
        st.stop()
    
    with st.chat_message("assistant"):
        with st.spinner("Menganalisis..."):
            tool_name = choose_tool(st.session_state.context_name, prompt)
            
            analysis_result = {}
            if tool_name == 'analyze_code':
                analysis_result = analyze_code(st.session_state.context_data)
            elif tool_name == 'parse_log':
                analysis_result = parse_log(st.session_state.context_data)
            elif tool_name == 'inspect_dependencies':
                analysis_result = inspect_dependencies(st.session_state.context_data)

            final_prompt = f"""KONTEKS ANALISIS:
- Nama Konteks: {st.session_state.context_name}
- Alat yang digunakan: {tool_name}
- Hasil Analisis Alat: {analysis_result or "Tidak ada analisis spesifik yang dijalankan."}
PERMINTAAN PENGGUNA: "{prompt}"
Tolong berikan jawaban yang komprehensif."""

            response_text = send_chat_message(st.session_state.chat, final_prompt)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})