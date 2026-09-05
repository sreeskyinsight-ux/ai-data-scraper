import streamlit as st
from openai import OpenAI
import datetime
import urllib.parse
import time

# --- IMPORT CREWAI ---
# Pastikan Anda sudah menginstal crewai: pip install crewai
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Konfigurasi Halaman (Tema Gelap Premium)
st.set_page_config(
    page_title="CyberIntel Enterprise - Multi-Agent Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Kustomisasi CSS Tingkat Lanjut (Ultimate SaaS Dark Theme v2.0)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background: #030712 !important;
        color: #f3f4f6 !important;
    }

    [data-testid="stSidebar"] {
        background: #0b0f19 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.1) !important;
        padding-top: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(56, 189, 248, 0.15) !important;
    }

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

    .stForm {
        background: rgba(15, 23, 42, 0.75) !important;
        padding: 32px !important;
        border-radius: 20px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 30px rgba(56, 189, 248, 0.05) !important;
        backdrop-filter: blur(16px) !important;
    }

    .stTextInput label, .stSelectbox label {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        margin-bottom: 6px !important;
    }

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

    .report-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 32px;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 15px 30px -10px rgba(0,0,0,0.5);
    }
    
    .agent-log {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #94a3b8;
        background: rgba(30, 41, 59, 0.4);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 0. FUNGSI & KONFIGURASI UTAMA ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = None

# Inisialisasi Database Pengguna di Session State
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@cyberintel.id": {"password": "adminpassword123", "role": "Administrator"},
        "agent@cyberintel.id": {"password": "password123", "role": "Agent"},
        "analis@cyberintel.id": {"password": "secret", "role": "Agent"}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.current_role = ""

if "history" not in st.session_state:
    st.session_state.history = []

# Konfigurasi Model LangChain/CrewAI (Opsional: Bisa disesuaikan per agen)
def get_llm(model_name="nousresearch/hermes-3-llama-3.1-70b"):
    if not api_key:
        st.error("OpenRouter API Key belum diset di secrets.")
        st.stop()
    return ChatOpenAI(
        model_name=model_name,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
    )

# --- A. FUNGSI PEMBUAT GAMBAR MANDIRI ---
def run_visual_generator(prompt_text):
    with st.spinner("🎨 Agen Artistik sedang merender visualisasi berdasarkan deskripsi..."):
        try:
            # Menggunakan layanan pembuatan gambar berbasis AI publik yang stabil via URL encoding
            encoded_prompt = urllib.parse.quote(prompt_text)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=123"
            return image_url
        except Exception as e:
            st.error(f"Gagal menghasilkan gambar: {e}")
            return None

# --- B. FUNGSI SISTEM MULTI-AGENT CREWAI ---
def run_agentic_research(topic):
    
    # 1. Tentukan Model untuk Agen
    llm_fast = get_llm("nousresearch/hermes-3-llama-3.1-70b") # Untuk kapten & peneliti cepat
    llm_writer = get_llm("anthropic/claude-3.5-sonnet") # Untuk penulis laporan yang lebih halus

    # 2. Definisikan Agen-Agen
    agent_researcher = Agent(
        role='Senior Data Analyst & Researcher',
        goal='Mengumpulkan data mendalam, tren terkini, dan fakta kunci terkait topik: {topic}',
        backstory="""Seorang analis data jenius dengan kemampuan riset web tingkat lanjut. Dikenal karena ketelitiannya dalam menyajikan data yang valid dan relevan.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_fast,
        # tools=[SerperDevTool()] # Opsional: Tambahkan tool pencarian nyata di sini jika punya keynya
    )

    agent_reporter = Agent(
        role='Senior Intelligence Reporter',
        goal='Menyusun data mentah dari Researcher menjadi laporan intelijen formal, tajam, dan terstruktur rapi berformat Markdown.',
        backstory="""Mantan jurnalis investigasi yang kini bekerja untuk agensi intelijen. Spesialis dalam menyusun narasi yang kuat dan berdampak dari data yang ada.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_writer
    )

    agent_artist = Agent(
        role='Creative Visual Strategist',
        goal='Menganalisis laporan yang dihasilkan dan membuatkan satu prompt deskriptif yang sangat detail, artistik, dan relevan untuk merender gambar ilustrasi konseptual yang menarik.',
        backstory="""Seorang direktur seni visioner yang mampu menerjemahkan data kompleks menjadi konsep visual yang estetis dan futuristik.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_fast # Menggunakan model yang cepat untuk membuat prompt gambar
    )

    # 3. Definisikan Tugas-Tugas
    task_gather = Task(
        description=f'Lakukan riset mendalam tentang "{topic}". Kumpulkan poin-poin data utama, tren pasar, dan konteks strategis.',
        expected_output='Ringkasan poin-poin data (bullet points) yang terstruktur, mencakup setidaknya 5 fakta penting.',
        agent=agent_researcher
    )

    task_report = Task(
        description=f'Berdasarkan data dari Researcher, susun laporan intelijen formal setidaknya 300 kata tentang "{topic}". Laporan harus memiliki judul, pendahuluan, analisis inti, dan kesimpulan.',
        expected_output='Laporan intelijen lengkap dalam format Markdown.',
        agent=agent_reporter,
        context=[task_gather]
    )

    task_visual = Task(
        description=f'Baca laporan yang disusun oleh Intelligence Reporter tentang "{topic}". Buatlah prompt teks bahasa Inggris yang sangat deskriptif (misal: gaya fotografi, pencahayaan, komposisi) untuk menghasilkan gambar ilustrasi konseptual yang mewakili esensi laporan tersebut.',
        expected_output='Satu kalimat panjang deskriptif yang kaya detail untuk digunakan sebagai prompt generator gambar AI.',
        agent=agent_artist,
        context=[task_report]
    )

    # 4. Bentuk Tim Crew & Jalankan
    crew = Crew(
        agents=[agent_researcher, agent_reporter, agent_artist],
        tasks=[task_gather, task_report, task_visual],
        process=Process.sequential, # Jalankan berurutan
        verbose=True,
        manager_llm=llm_fast # Hermes sebagai manajer tim
    )

    # 5. Eksekusi & Tangkap Log Output
    with st.spinner(f"🤖 Multi-Agent CrewAI sedang bekerja secara otonom pada topik: {topic}..."):
        try:
            # Tampilkan log progress secara langsung di Streamlit
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text("Memulai investigasi multi-agen...")
            
            # CrewAI menjalankan tugas secara berurutan
            result = crew.kickoff()
            
            progress_bar.progress(100)
            status_text.text("Investigasi multi-agen selesai.")
            
            # Mengambil hasil akhir dari setiap task
            final_report = task_report.output.raw
            visual_prompt = task_visual.output.raw
            
            return final_report, visual_prompt
            
        except Exception as e:
            st.error(f"Terjadi kesalahan selama eksekusi CrewAI: {e}")
            return None, None

# --- HALAMAN LOGIN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🛡️</div>
                <h1 style='font-size: 2.2rem !important;'>CyberIntel Enterprise</h1>
                <p style='color: #94a3b8; font-size: 0.95rem;'>Agentic AI Command & Visual Center</p>
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
                
        st.markdown("<p style='text-align:center; color:#64748b; font
