# 🤖 CodeGuardian v4: Agent Analisis Cerdas
Final Project AI for Data Scientist x Hacktiv8
Sebuah aplikasi web cerdas berbasis AI Agent yang berfungsi sebagai asisten untuk menganalisis kode, file log, dan dependensi proyek perangkat lunak. Proyek ini dibangun menggunakan Python, Streamlit, dan ditenagai oleh Google Gemini API.

---

# 🌐 Streamlit : Web App is deployed and accessible worldwide

https://final-aidata-cguardian.streamlit.app/

---

## ✨ Fitur Utama

-   **Analisis Multi-Konteks**: Mampu menganalisis berbagai jenis file teknis:
    -   **Kode Python (`.py`)**: Memberikan ringkasan statistik (jumlah baris, fungsi) dan menjelaskan fungsi.
    -   **File Log (`.log`, `.txt`)**: Mendeteksi, menghitung, dan meringkas pesan error atau warning.
    -   **Dependensi (`requirements.txt`)**: Mendaftar dan menjelaskan pustaka yang digunakan dalam proyek.
-   **Arsitektur AI Agent Cerdas**: Menggunakan model AI untuk memilih "alat" analisis yang paling tepat secara dinamis berdasarkan konteks file dan permintaan pengguna.
-   **Input Ganda**: Pengguna dapat memberikan konteks dengan dua cara yang fleksibel:
    1.  **Unggah File**: Mengunggah file langsung dari komputer.
    2.  **Paste Teks**: Menyalin dan menempelkan potongan kode atau log langsung ke dalam aplikasi.
-   **Memori Percakapan**: Sesi chat bersifat kontekstual. Agent dapat mengingat pertanyaan sebelumnya dalam satu sesi untuk memberikan jawaban yang relevan dan berkelanjutan.
-   **Manajemen API Key yang Aman**: Pengguna memasukkan Gemini API Key mereka langsung di antarmuka, yang disimpan sementara dalam sesi dan tidak diekspos secara publik. Form input akan disembunyikan setelah key berhasil disimpan.

---

## 🏛️ Arsitektur Proyek

Proyek ini dibangun dengan prinsip **Separation of Concerns**, memisahkan logika ke dalam empat modul yang berbeda untuk keterbacaan dan pengelolaan yang lebih baik:

| File           | Peran (Tanggung Jawab)                                        |
| :-----------   | :------------------------------------------------------------ |
| **`app.py`**   | **Antarmuka Pengguna (UI) & Orkestrator**<br>Mengelola semua elemen visual Streamlit dan alur kerja utama aplikasi. |
| **`agent.py`** | **Otak Pengambil Keputusan**<br>Bertugas memilih alat analisis yang paling sesuai untuk permintaan pengguna. |
| **`tools.py`** | **Eksekutor Tugas Spesifik (Kotak Peralatan)**<br>Berisi semua fungsi untuk melakukan analisis (misalnya, `parse_log`, `analyze_code`). |
| **`chat.py`**  | **Manajer Percakapan**<br>Menangani semua interaksi langsung dengan Google Gemini API dan mengelola sesi chat. |

---

## 🛠️ Teknologi yang Digunakan

-   **Bahasa**: Python 3.9+
-   **Framework Aplikasi Web**: Streamlit
-   **Model AI**: Google Gemini API (`gemini-1.5-flash`)
-   **Library Pendukung**: `google-generativeai`, `python-dotenv`

---

## 🚀 Pengaturan & Instalasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

### 1. Prasyarat

-   Python 3.9 atau yang lebih baru
-   API Key dari [Google AI Studio](https://aistudio.google.com/)

### 2. Kloning Repositori

```bash
git clone [https://github.com/your-username/codeguardian.git](https://github.com/your-username/codeguardian.git)

cd codeguardian
