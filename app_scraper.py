import streamlit as st
from openai import OpenAI
import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="CyberIntel AI - Intelligence Agency",
    page_icon="🛡️",
    layout="wide"
)

# Kustomisasi CSS Tingkat Lanjut (Modern Dark Cyber-Enterprise Theme)
st.markdown("""
    <style>
    /* Import Google Fonts - Inter & Fira Code */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Latar belakang utama dengan gradien halus */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #0f172a 100%);
        color: #f1f5f9;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0b0f19 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.15);
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(56, 189, 248, 0.2);
    }

    /* Header & Judul Utama */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    
    h1 {
        font-size: 2.2rem !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Kotak Form Utama */
    .stForm {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }

    /* Label Input */
    .stTextInput label, .stSelectbox label {
        color: #38bdf8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em;
    }

    /* Kotak Input Teks & Selectbox */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* Tombol Utama (Jalankan Operasi / Masuk Sistem) */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        padding: 10px 24px !important;
        font-size: 0.95rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
        letter-spacing: 0.025em;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
        box-shadow: 0 6px 16px rgba(56, 189, 248, 0.4);
        transform: translateY(-1px);
    }

    /* Tombol Download Laporan */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
        color: #ffffff !important;
        padding: 6px 16px !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(13, 148, 136, 0.3);
    }
    
    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
        transform: translateY(-1px);
    }

    /* Kartu Profil Sidebar & Kotak Hasil Laporan */
    .report-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        padding: 24px;
        border-radius: 12px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Inisialisasi Database Pengguna di Session State
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@cyberintel.id": {"password": "adminpassword123", "role": "Administrator"},
        "agent@cyberintel.id": {"password": "password123", "role": "Agent"}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.current_role = ""

if "history" not in st.session_state:
    st.session_state.history = []

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'><h1>🛡️ CyberIntel AI</h1><p style='color: #94a3b8; font-size: 1rem; margin-top: -10px;'>Secure Intelligence & Web Scraper System</p></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Shortcut Demo Akses Cepat
        st.info("💡 **Akses Cepat Demo:** Pilih akun di bawah untuk login instan:")
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            if st.button("🔑 Login Admin"):
                st.session_state.logged_in = True
                st.session_state.current_user = "admin@cyberintel.id"
                st.session_state.current_role = "Administrator"
                st.rerun()
        with dcol2:
            if st.button("🔑 Login Agent"):
                st.session_state.logged_in = True
                st.session_state.current_user = "agent@cyberintel.id"
                st.session_state.current_role = "Agent"
                st.rerun()
                
        st.markdown("<p style='text-align:center; color:#64748b; font-size:0.85rem; margin: 15px 0;'>Atau gunakan email pribadi Anda:</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username_input = st.text_input("Alamat Email", placeholder="contoh: sree.skyinsight@gmail.com")
            password_input = st.text_input("Password", type="password", placeholder="Masukkan password bebas")
            login_btn = st.form_submit_button("Masuk Sistem")
            
            if login_btn:
                if username_input.strip() != "":
                    if username_input not in st.session_state.users_db:
                        st.session_state.users_db[username_input] = {
                            "password": password_input if password_input else "123456",
                            "role": "Agent"
                        }
                    
                    st.session_state.logged_in = True
                    st.session_state.current_user = username_input
                    st.session_state.current_role = st.session_state.users_db[username_input]["role"]
                    st.success("Otorisasi Berhasil! Memuat sistem...")
                    st.rerun()
                else:
                    st.error("Alamat Email tidak boleh kosong!")
        st.stop()

# --- HALAMAN UTAMA SETELAH LOGIN ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = None

with st.sidebar:
    st.markdown(f"### 🛡️ CyberIntel Agency")
    st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.8); padding: 12px; border-radius: 8px; border: 1px solid rgba(56, 189, 248, 0.2); margin-bottom: 20px;'>
            <p style='margin: 0; font-size: 0.75rem; color: #94a3b8;'>TEROTORISASI SEBAGAI:</p>
            <p style='margin: 4px 0 0 0; font-size: 0.9rem; font-weight: 600; color: #38bdf8; word-break: break-all;'>{st.session_state.current_user}</p>
            <span style='display: inline-block; margin-top: 8px; background: #0284c7; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600;'>{st.session_state.current_role}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Keluar Sistem"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.divider()
    st.markdown("### ⚙️ Konfigurasi Sistem")
    
    selected_model = st.selectbox(
        "Model Agen AI:",
        [
            "nousresearch/hermes-3-llama-3.1-70b", 
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ]
    )
    
    st.divider()
    st.markdown("### 📂 Arsip Kasus")
    if len(st.session_state.history) == 0:
        st.caption("Belum ada arsip investigasi tersimpan.")
    else:
        for i, item in enumerate(st.session_state.history):
            if st.button(f"📁 {item['target'][:22]}...", key=f"hist_{i}"):
                st.session_state.active_report = item['result']
                st.session_state.active_target = item['target']

    if st.session_state.current_role == "Administrator":
        st.divider()
        st.markdown("### 🛠️ Admin Panel")
        with st.expander("Kelola Pengguna"):
            st.write("Database Agen Aktif:")
            for u, data in st.session_state.users_db.items():
                st.text(f"• {u} ({data['role']})")
            
            new_user = st.text_input("Email Baru", placeholder="nama@domain.com")
            new_pass = st.text_input("Password Baru", type="password")
            if st.button("Tambah Agen Baru"):
                if new_user and new_pass:
                    st.session_state.users_db[new_user] = {
                        "password": new_pass, 
                        "role": "Agent"
                    }
                    st.success(f"Agen {new_user} ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Lengkapi data form.")

# Tampilan Konten Utama
st.markdown("<h1>🕵️‍♂️ CyberIntel AI: Web Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.05rem; margin-top: -10px; margin-bottom: 25px;'>Sistem investigasi berbasis AI cerdas untuk ekstraksi data web, riset kompetitor, dan analisis intelijen mendalam.</p>", unsafe_allow_html=True)

with st.form("scraper_form"):
    target_query = st.text_input(
        "Target Investigasi / Topik Web:",
        placeholder="Contoh: Analisis tren perilaku konsumen digital terbaru"
    )
    
    task_type = st.selectbox(
        "Protokol Investigasi:",
        ["Rangkuman Intelijen Berita", "Ekstraksi Data & Profiling Kompetitor", "Analisis Dokumen Mendalam"]
    )
    
    submitted = st.form_submit_button("🔍 Jalankan Operasi Intelijen")

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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 🗂️ Berkas Laporan: *{st.session_state.get('active_target', '')}*")
    with col2:
        st.download_button(
            label="📥 Unduh Laporan (.md)",
            data=st.session_state.active_report,
            file_name=f"laporan_cyberintel_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    st.divider()
    st.markdown(st.session_state.active_report)
    st.markdown('</div>', unsafe_allow_html=True)
