import streamlit as st
import os
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Pano Elemanı Testi (PNG)", page_icon="🖼️")

# --- CEVAP ANAHTARI (1.png'den 24.png'ye kadar) ---
# Kendi resim sıralamana göre buradaki isimleri düzenle.
CEVAP_ANAHTARI = {
    "1": "Bir fazlı sigorta",
    "2": "Üç fazlı sigorta",
    "3": "NH bıçaklı sigorta",
    "4": "Kaçak akım rölesi",
    "5": "Üç fazlı paket şalter",
    "6": "Termik manyetik şalter",
    "7": "Akım transformatörü",
    "8": "Bir fazlı aktif sayaç",
    "9": "Üç fazlı aktif sayaç",
    "10": "Üç fazlı kombi sayaç",
    "11": "Ampermetre",
    "12": "Voltmetre",
    "13": "Sinyal lambası",
    "14": "Start butonu",
    "15": "Stop butonu",
    "16": "Jog buton",
    "17": "Aşırı akım rölesi",
    "18": "Motor koruma şalteri",
    "19": "Kontaktör",
    "20": "Zaman rölesi",
    "21": "Motor koruma rölesi",
    "22": "Faz sırası rölesi",
    "23": "Kondansatör",
    "24": "Alçak gerilim parafudr"
}

# --- AYARLAR ---
KLASOR_ADI = "yeni klasör"

# Session State Yönetimi
if 'soru_no' not in st.session_state:
    st.session_state.soru_no = 1
if 'durum' not in st.session_state:
    st.session_state.durum = None

def kontrol():
    tahmin = st.session_state.tahmin_input.lower().strip()
    dogru_cevap = CEVAP_ANAHTARI[str(st.session_state.soru_no)].lower()
    
    # Esnek kontrol (Tahmin doğru cevabın içinde geçiyorsa doğru say)
    if tahmin in dogru_cevap and len(tahmin) > 2:
        st.session_state.durum = "dogru"
    else:
        st.session_state.durum = "yanlis"

def sonraki():
    if st.session_state.soru_no < 24:
        st.session_state.soru_no += 1
    else:
        st.session_state.soru_no = 1 # 24 bitince başa dön
    st.session_state.durum = None
    st.session_state.tahmin_input = ""

# --- ARAYÜZ ---
st.title("⚡ Pano Elemanlarını Tanıyalım (PNG Versiyon)")
st.divider()

# Dinamik Dosya Yolu (1.png, 2.png...)
resim_adi = f"{st.session_state.soru_no}.png"
resim_yolu = os.path.join(KLASOR_ADI, resim_adi)

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"### Soru: {st.session_state.soru_no} / 24")
    if os.path.exists(resim_yolu):
        img = Image.open(resim_yolu)
        st.image(img, use_container_width=True, caption=f"Dosya: {resim_adi}")
    else:
        st.error(f"⚠️ Hata: '{resim_yolu}' bulunamadı! Lütfen klasör adını ve dosya formatını kontrol et.")

with col2:
    st.text_input("Bu hangi pano elemanı?", key="tahmin_input", on_change=kontrol)
    
    if st.session_state.durum == "dogru":
        st.success(f"HARİKA! ✅\n\nCevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Sonraki Görsele Geç ➡️", on_click=sonraki)
        st.balloons()
        
    elif st.session_state.durum == "yanlis":
        st.error(f"YANLIŞ! ❌\n\nDoğru cevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Devam Et ➡️", on_click=sonraki)

st.divider()
st.info("İpucu: Tahminini yazıp Enter'a basabilirsin.")
