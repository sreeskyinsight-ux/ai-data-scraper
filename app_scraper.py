import streamlit as st
from openai import OpenAI
import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="CyberIntel AI - Enterprise Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Kustomisasi CSS Tingkat Lanjut (Ultimate SaaS Dark Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Background */
    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background: #030712 !important;
        color: #f3f4f6 !important;
    }

    /* Sidebar Styling Premium */
    [data-testid="stSidebar"] {
        background: #0b0f19 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.1) !important;
        padding-top: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(56, 189, 248, 0.15) !important;
    }

    /* Header & Judul Utama */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
    }
    
    h1 {
        font-size: 2.4rem !important;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem !important;
    }

    /* Card Box Utama / Form Container */
    .stForm {
        background: rgba(15, 23, 42, 0.75) !important;
        padding: 32px !important;
        border-radius: 20px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 30px rgba(56, 189, 248, 0.05) !important;
        backdrop-filter: blur(16px) !important;
    }

    /* Label Input Form yang Jelas & Terang */
    .stTextInput label, .stSelectbox label {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 6px !important;
    }

    /* Kotak Input Teks & Selectbox */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #030712 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
    }

    /* Tombol Eksekusi / Submit Utama */
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        box-shadow: 0 10px 25px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* Kartu Kontainer Hasil Laporan / Gambar */
    .report-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 32px;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 15px 30px -10px rgba(0,0,0,0.5);
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
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🛡️</div>
                <h1 style='font-size: 2.2rem !important;'>CyberIntel AI</h1>
                <p style='color: #94a3b8; font-size: 0.95rem;'>Enterprise Intelligence & Visual Generator System</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("⚡ **Akses Cepat Demo (Instan):**")
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
                
        st.markdown("<p style='text-align:center; color:#64748b; font-size:0.85rem; margin: 20px 0 10px 0;'>Atau gunakan email pribadi Anda:</p>", unsafe_allow_html=True)
        
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
    st.markdown("### 🛡️ CyberIntel Agency")
    st.markdown(f"""
        <div style='background: rgba(30, 41, 59, 0.6); padding: 14px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.2); margin: 15px 0;'>
            <p style='margin: 0; font-size: 0.7rem; color: #94a3b8; font-weight: 700; letter-spacing: 0.05em;'>AGEN TEROTORISASI:</p>
            <p style='margin: 6px 0 0 0; font-size: 0.85rem; font-weight: 600; color: #38bdf8; word-break: break-all;'>{st.session_state.current_user}</p>
            <div style='margin-top: 8px;'>
                <span style='background: #0284c7; color: #fff; padding: 2px 8px; border-radius: 6px; font-size: 0.65rem; font-weight: 700;'>{st.session_state.current_role}</span>
            </div>
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
    st.markdown("### 📂 Arsip Investigasi")
    if len(st.session_state.history) == 0:
        st.caption("Belum ada arsip tersimpan.")
    else:
        for i, item in enumerate(st.session_state.history):
            icon = "🎨" if item['type'] == "image" else "📁"
            if st.button(f"{icon} {item['target'][:18]}...", key=f"hist_{i}"):
                st.session_state.active_result = item['result']
                st.session_state.active_target = item['target']
                st.session_state.active_type = item['type']

# Tampilan Konten Utama
st.markdown("<h1>🕵️‍♂️ CyberIntel AI: Web & Visual Suite</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.05rem; margin-bottom: 30px;'>Sistem investigasi berbasis AI cerdas untuk ekstraksi data web, analisis mendalam, serta pembuatan gambar visual operasional.</p>", unsafe_allow_html=True)

with st.form("scraper_form"):
    target_query = st.text_input(
        "Target Investigasi / Deskripsi Gambar:",
        placeholder="Contoh: Desain konsep futuristik kota cyber intelijen modern"
    )
    
    task_type = st.selectbox(
        "Protokol Operasi:",
        [
            "Rangkuman Intelijen Berita", 
            "Ekstraksi Data & Profiling Kompetitor", 
            "Analisis Dokumen Mendalam",
            "🎨 Pembuat Gambar AI (Visual Generator)"
        ]
    )
    
    submitted = st.form_submit_button("🚀 Jalankan Operasi")

if submitted:
    if not api_key:
        st.warning("⚠️ Kesalahan Sistem: OpenRouter API Key belum dikonfigurasi di secrets.")
    elif not target_query:
        st.warning("⚠️ Mohon masukkan target investigasi atau deskripsi gambar terlebih dahulu.")
    else:
        if task_type == "🎨 Pembuat Gambar AI (Visual Generator)":
            with st.spinner("🎨 Agen sedang merender gambar visual via DALL-E 3..."):
                try:
                    # Menggunakan klien OpenAI untuk memanggil DALL-E 3
                    client_img = OpenAI(api_key=api_key)
                    response_img = client_img.images.generate(
                        model="dall-e-3",
                        prompt=target_query,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = response_img.data[0].url
                    
                    st.session_state.history.insert(0, {
                        "target": target_query,
                        "result": image_url,
                        "type": "image",
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.session_state.active_result = image_url
                    st.session_state.active_target = target_query
                    st.session_state.active_type = "image"
                except Exception as e:
                    st.error(f"Gagal menghasilkan gambar. Pastikan API key Anda mendukung DALL-E 3: {e}")
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
                        "type": "text",
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    
                    st.session_state.active_result = hasil_ai
                    st.session_state.active_target = target_query
                    st.session_state.active_type = "text"
                    
                except Exception as e:
                    st.error(f"Gagal terhubung ke jaringan AI: {e}")

if "active_result" in st.session_state:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    if st.session_state.get("active_type") == "image":
        st.markdown(f"### 🎨 Hasil Render Visual: *{st.session_state.get('active_target', '')}*")
        st.divider()
        st.image(st.session_state.active_result, caption=st.session_state.get('active_target', ''), use_container_width=True)
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🗂️ Berkas Laporan: *{st.session_state.get('active_target', '')}*")
        with col2:
            st.download_button(
                label="📥 Unduh Laporan (.md)",
                data=st.session_state.active_result,
                file_name=f"laporan_cyberintel_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        st.divider()
        st.markdown(st.session_state.active_result)
    st.markdown('</div>', unsafe_allow_html=True)
