import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(
    page_title="Detective AI - Data & Research Intelligence",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Kustomisasi Tema Detektif (Dark Slate, Deep Blue, & Steel Accent) menggunakan CSS
st.markdown("""
    <style>
    /* Mengubah latar belakang utama dan sidebar */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Sidebar kustom ala investigasi */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Styling Header & Teks */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Styling Kotak Form & Kartu */
    .stForm {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    
    /* Tombol Khas Investigasi */
    .stButton>button {
        background-color: #0284c7;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# Judul Aplikasi Ala Detektif
st.title("🕵️‍♂️ Detective AI: Intelligence & Research Agency")
st.markdown("Pekerjakan agen intelijen AI untuk menyelidiki, mengumpulkan, dan menganalisis data web secara mendalam.")

# Sidebar untuk Pengaturan & Simulasi Kuota SaaS
with st.sidebar:
    st.header("⚙️ Kontrol Investigasi")
    
    # Mengambil API key secara aman di belakang layar (tanpa kotak hijau)
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        api_key = None
    
    # Pilihan Model AI (Termasuk Hermes)
    selected_model = st.selectbox(
        "Pilih Agen Model (Hermes/LLM):",
        [
            "nousresearch/hermes-3-llama-3.1-70b", 
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ]
    )
    
    st.divider()
    st.info("💡 **Status SaaS:** Level Agen (Sisa Kuota: 3/3 Penyelidikan)")
    st.button("Upgrade ke Level Senior Detective")

# Area Utama (Form Input)
st.subheader("🎯 Berikan Kasus / Target Riset")

with st.form("scraper_form"):
    target_query = st.text_input(
        "Apa target investigasi atau topik yang ingin di-scraping?",
        placeholder="Contoh: Analisis mendalam celah pasar produk digital di 2026"
    )
    
    task_type = st.selectbox(
        "Pilih Protokol Investigasi:",
        ["Rangkuman Intelijen Berita", "Ekstraksi Data & Profiling Kompetitor", "Analisis Dokumen Mendalam"]
    )
    
    submitted = st.form_submit_button("🔍 Jalankan Operasi AI")

if submitted:
    if not api_key:
        st.warning("⚠️ Kesalahan Sistem: OpenRouter API Key belum dikonfigurasi di secrets.")
    elif not target_query:
        st.warning("⚠️ Mohon masukkan target investigasi terlebih dahulu.")
    else:
        with st.spinner(f"🕵️‍♂️ Agen {selected_model} sedang melacak dan mengumpulkan data dari web..."):
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
                
                st.success("✅ Operasi Intelijen Selesai!")
                st.markdown("### 🗂️ Berkas Laporan Investigasi:")
                st.markdown(hasil_ai)
                
            except Exception as e:
                st.error(f"Gagal terhubung ke pusat jaringan AI: {e}")
