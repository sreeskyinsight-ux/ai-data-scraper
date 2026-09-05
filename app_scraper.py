import streamlit as st
from openai import OpenAI
import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="CyberIntel AI - Intelligence Agency",
    page_icon="🛡️",
    layout="wide"
)

# Kustomisasi CSS Profesional & Elegan (Memperbaiki Warna Tombol & Kontras)
st.markdown("""
    <style>
  st.markdown("""
    <style>
    /* Latar belakang utama */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #1e1b4b;
        border-right: 1px solid #312e81;
    }
    
    /* Header & Judul */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Kartu & Container Form */
    .stForm {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    
    /* Perbaikan Mutlak Tombol: Latar Biru Terang & Teks Gelap Kontras */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        padding: 6px 18px !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #7dd3fc !important;
        color: #0f172a !important;
    }
    
    /* Tombol Download */
    div.stDownloadButton > button {
        background-color: #0d9488 !important;
        color: #ffffff !important;
        padding: 4px 12px !important;
        font-size: 12px !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #0f766e !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Inisialisasi Database Pengguna di Session State (Termasuk Akun Admin)
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "adminpassword123", "role": "Administrator", "joined": "2026-06-01"},
        "detektif1": {"password": "password123", "role": "Agent", "joined": "2026-06-05"}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.current_role = ""

if "history" not in st.session_state:
    st.session_state.history = []

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🛡️ CyberIntel Secure Login")
        st.caption("Masukkan kredensial otorisasi agen Anda.")
        
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Masuk Sistem")
            
            if login_btn:
                if username_input in st.session_state.users_db and st.session_state.users_db[username_input]["password"] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username_input
                    st.session_state.current_role = st.session_state.users_db[username_input]["role"]
                    st.success("Otorisasi Berhasil! Memuat sistem...")
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")
        st.stop()

# --- HALAMAN UTAMA SETELAH LOGIN ---

# Mengambil API key secara aman
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = None

# Sidebar Kontrol & Admin Panel
with st.sidebar:
    st.markdown(f"👤 **Agent:** `{st.session_state.current_user}`")
    st.markdown(f"🏷️ **Role:** `{st.session_state.current_role}`")
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.divider()
    st.header("⚙️ Konfigurasi")
    
    selected_model = st.selectbox(
        "Pilih Model Agen:",
        [
            "nousresearch/hermes-3-llama-3.1-70b", 
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ]
    )
    
    st.divider()
    st.subheader("📂 Arsip Kasus")
    if len(st.session_state.history) == 0:
        st.caption("Belum ada arsip investigasi.")
    else:
        for i, item in enumerate(st.session_state.history):
            if st.button(f"📁 {item['target'][:20]}...", key=f"hist_{i}"):
                st.session_state.active_report = item['result']
                st.session_state.active_target = item['target']

    # --- FITUR KHUSUS ADMIN: MANAJEMEN USER ---
    if st.session_state.current_role == "Administrator":
        st.divider()
        st.subheader("🛠️ Admin Panel: Database User")
        with st.expander("Kelola Pengguna"):
            st.write("Daftar Agen Terdaftar:")
            for u, data in st.session_state.users_db.items():
                st.text(f"- {u} ({data['role']})")
            
            new_user = st.text_input("Username Baru")
            new_pass = st.text_input("Password Baru", type="password")
            if st.button("Tambah Agen Baru"):
                if new_user and new_pass:
                    st.session_state.users_db[new_user] = {
                        "password": new_pass, 
                        "role": "Agent", 
                        "joined": str(datetime.date.today())
                    }
                    st.success(f"Agen {new_user} berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Isi lengkap username & password.")

# Konten Utama Aplikasi
st.title("🕵️‍♂️ CyberIntel AI: Web Intelligence & Scraper")
st.markdown("Sistem investigasi berbasis AI cerdas untuk ekstraksi data web, riset kompetitor, dan analisis mendalam.")

with st.form("scraper_form"):
    target_query = st.text_input(
        "Target Investigasi / Topik Web:",
        placeholder="Contoh: Analisis tren harga produk digital terlaris"
    )
    
    task_type = st.selectbox(
        "Protokol Investigasi:",
        ["Rangkuman Intelijen Berita", "Ekstraksi Data & Profiling Kompetitor", "Analisis Dokumen Mendalam"]
    )
    
    submitted = st.form_submit_button("🔍 Jalankan Operasi")

if submitted:
    if not api_key:
        st.warning("⚠️ Kesalahan Sistem: OpenRouter API Key belum dikonfigurasi di secrets.")
    elif not target_query:
        st.warning("⚠️ Mohon masukkan target investigasi terlebih dahulu.")
    else:
        with st.spinner(f"🛡️ Agen sedang mengeksekusi investigasi via {selected_model}..."):
            try:
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )
                
                prompt = f"""
                Bertindaklah sebagai Detektif Data Senior dan Kepala Intelijen Riset Profesional.
                Protokol Tugas: {task_type}
                Target Investigasi: {target_query}
                
                Berikan laporan investigasi yang tajam, mendalam, berbasis data, dan terstruktur rapi menggunakan format markdown ala laporan intelijen profesional.
                """
                
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "Kamu adalah agen intelijen data dan riset profesional yang analitis."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                hasil_ai = response.choices[0].message.content
                
                st.session_state.history.insert(0, {
                    "target": target_query,
                    "result": hasil_ai,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.session_state.active_report = hasil_ai
                st.session_state.active_target = target_query
                
            except Exception as e:
                st.error(f"Gagal terhubung ke jaringan AI: {e}")

if "active_report" in st.session_state:
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 🗂️ Berkas Laporan: *{st.session_state.get('active_target', '')}*")
    with col2:
        st.download_button(
            label="📥 Unduh Laporan",
            data=st.session_state.active_report,
            file_name=f"laporan_cyberintel_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    st.markdown(st.session_state.active_report)
