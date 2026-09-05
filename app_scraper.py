import streamlit as st
from openai import OpenAI

# Konfigurasi Halaman
st.set_page_config(
    page_title="AI Data Scraper Agent",
    page_icon="🤖",
    layout="wide"
)

# Judul Aplikasi
st.title("🤖 AI Karyawan Otomatis: Web Data & Research Scraper")
st.markdown("Pekerjakan agen AI untuk mencari, mengambil, dan merangkum data dari internet secara otomatis.")

# Sidebar untuk Pengaturan & Simulasi Kuota SaaS
with st.sidebar:
    st.header("⚙️ Pengaturan Agen")
    
    # Mengambil API key secara otomatis dari secrets.toml
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.success("✅ API Key Berhasil Dimuat Aman")
    except Exception:
        api_key = None
        st.error("❌ API Key belum diatur di secrets.toml!")
    
    # Pilihan Model AI (Termasuk Hermes)
    selected_model = st.selectbox(
        "Pilih Model AI / Hermes:",
        [
            "nousresearch/hermes-3-llama-3.1-70b", # Model Hermes di OpenRouter
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o"
        ]
    )
    
    st.divider()
    st.info("💡 **Status SaaS:** Akun Trial (Sisa Kuota: 3/3 Tugas)")
    st.button("Upgrade ke Paket Pro")

# Area Utama (Form Input)
st.subheader("🎯 Berikan Tugas ke Karyawan AI")

with st.form("scraper_form"):
    target_query = st.text_input(
        "Apa yang ingin dicari atau di-scraping dari internet?",
        placeholder="Contoh: produk digital apa yang paling cuan saat ini?"
    )
    
    task_type = st.selectbox(
        "Pilih Jenis Tugas:",
        ["Rangkuman Berita & Tren", "Ekstraksi Data / Riset Kompetitor", "Analisis Artikel Panjang"]
    )
    
    submitted = st.form_submit_button("🚀 Jalankan Agen AI")

if submitted:
    if not api_key:
        st.warning("⚠️ Mohon atur OpenRouter API Key terlebih dahulu di dalam file `secrets.toml`.")
    elif not target_query:
        st.warning("⚠️ Mohon masukkan topik atau target pencarian.")
    else:
        with st.spinner(f"🤖 Karyawan AI menggunakan model {selected_model} sedang bekerja..."):
            try:
                # Inisialisasi Client OpenRouter
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )
                
                # Prompt instruksi untuk AI
                prompt = f"""
                Bertindaklah sebagai Karyawan AI Profesional dan Ahli Riset Data.
                Tugas yang diberikan: {task_type}
                Topik/Target: {target_query}
                
                Berikan laporan analisis yang mendalam, terstruktur dengan rapi menggunakan format markdown, dan berikan poin-poin penting yang profesional.
                """
                
                # Memanggil API OpenRouter
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "Kamu adalah agen riset data profesional yang cerdas dan handal."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                hasil_ai = response.choices[0].message.content
                
                st.success("✅ Tugas selesai!")
                st.markdown("### 📄 Hasil Laporan Karyawan AI:")
                st.markdown(hasil_ai)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungkan ke AI: {e}")