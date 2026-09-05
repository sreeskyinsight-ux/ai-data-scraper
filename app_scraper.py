import streamlit as st
from openai import OpenAI
import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Detective AI - Intelligence Agency",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Kustomisasi CSS Profesional & Elegan (Tombol Proporsional & Estetika Dark Detective)
st.markdown("""
    <style>
    /* Latar belakang utama dan sidebar */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    /* Header */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Kotak Form Utama */
    .stForm {
        background-color: #111827;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
    
    /* Ukuran Tombol yang Proporsional & Elegan */
    .stButton>button {
        background-color: #0284c7;
        color: white;
        padding: 6px 16px;
        font-size: 14px;
        border-radius: 6px;
        border: none;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: #ffffff;
    }
    
    /* Styling Download Button agar serasi */
    .stDownloadButton>button {
        background-color: #334155;
        color: #f8fafc;
        padding: 4px 12px;
        font-size: 13px;
        border-radius: 6px;
        border: 1px solid #475569;
    }
    .stDownloadButton>button:hover {
        background-color: #475569;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Session State untuk Menyimpan Riwayat Investigasi
if "history" not in st.session_state:
    st.session_state.history = []

# Judul Aplikasi
st.title("🕵️‍♂️ Detective AI: Intelligence & Research Agency")
st.markdown("Pusat intelijen berbasis AI untuk investigasi mendalam, ekstraksi data web, dan analisis kompetitor.")

# Mengambil API key secara aman di belakang layar
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = None

# Sidebar: Kontrol & Riwayat Investigasi
with st.sidebar:
    st.header("⚙️ Kontrol Operasi")
    
    selected_model = st.selectbox(
        "Pilih Model Agen:",
        [
            "nousresearch/hermes-3-llama-3.1-70b", 
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ]
    )
    
    st.divider()
    st.subheader("📂 Arsip Kasus (History)")
    
    if len(st.session_state.history) == 0:
        st.caption("Belum ada investigasi tersimpan.")
    else:
        for i, item in enumerate(st.session_state.history):
            if st.button(f"📁 {item['target'][:22]}...", key=f"hist_{i}"):
                st.session_state.active_report = item['result']
                st.session_state.active_target = item['target']

    st.divider()
    st.info("💡 **Status SaaS:** Akun Agen Aktif")

# Area Utama (Form Input)
st.subheader("🎯 Berikan Kasus / Target Riset")

with st.form("scraper_form"):
    target_query = st.text_input(
        "Target Investigasi / Topik:",
        placeholder="Contoh: Tren produk digital paling menguntungkan tahun ini"
    )
    
    task_type = st.selectbox(
        "Protokol Investigasi:",
        ["Rangkuman Intelijen Berita", "Ekstraksi Data & Profiling Kompetitor", "Analisis Dokumen Mendalam"]
    )
    
    # Tombol submit yang ukurannya sudah diproporsionalkan via CSS
    submitted = st.form_submit_button("🔍 Jalankan Operasi AI")

if submitted:
    if not api_key:
        st.warning("⚠️ Kesalahan Sistem: OpenRouter API Key belum dikonfigurasi di secrets.")
    elif not target_query:
        st.warning("⚠️ Mohon masukkan target investigasi terlebih dahulu.")
    else:
        with st.spinner(f"🕵️‍♂️ Melacak dan menganalisis data menggunakan {selected_model}..."):
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
                
                # Simpan ke Session State History
                st.session_state.history.insert(0, {
                    "target": target_query,
                    "result": hasil_ai,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                st.session_state.active_report = hasil_ai
                st.session_state.active_target = target_query
                
            except Exception as e:
                st.error(f"Gagal terhubung ke pusat jaringan AI: {e}")

# Menampilkan Laporan Aktif (Hasil Baru atau dari Riwayat)
if "active_report" in st.session_state:
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 🗂️ Berkas Laporan: *{st.session_state.get('active_target', '')}*")
    with col2:
        # Tombol Download Laporan agar profesional
        st.download_button(
            label="📥 Unduh Laporan",
            data=st.session_state.active_report,
            file_name=f"laporan_investigasi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    st.markdown(st.session_state.active_report)
