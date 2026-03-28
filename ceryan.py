import streamlit as st
import os
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Pano Elemanı Testi", page_icon="🔌")

# --- 1'DEN 24'E KADAR EŞLEŞTİRME LİSTESİ ---
# Buradaki cevapları senin klasöründeki numara sırasına göre düzenleyebilirsin.
CEVAP_ANAHTARI = {
    "1": "Bir fazlı sigorta",
    "2": "Üç fazlı sigorta",
    "3": "Kaçak akım rölesi",
    "4": "Kontaktör",
    "5": "Termik röle",
    "6": "Zaman rölesi",
    "7": "Motor koruma şalteri",
    "8": "Sinyal lambası",
    "9": "Start butonu",
    "10": "Stop butonu",
    "11": "Acil durdurma butonu",
    "12": "Pako şalter",
    "13": "Akım transformatörü",
    "14": "Klemens",
    "15": "Ray",
    "16": "Kablo kanalı",
    "17": "Ampermetre",
    "18": "Voltmetre",
    "19": "Faz sırası rölesi",
    "20": "Sıvı seviye rölesi",
    "21": "Fotosel röle",
    "22": "Kondansatör",
    "23": "Parafudr",
    "24": "Şebeke jeneratör enversör şalter"
}

# --- AYARLAR ---
KLASOR_ADI = "yeni klasör"

# Session State
if 'soru_no' not in st.session_state:
    st.session_state.soru_no = 1
if 'durum' not in st.session_state:
    st.session_state.durum = None

def kontrol():
    tahmin = st.session_state.tahmin_input.lower().strip()
    dogru_cevap = CEVAP_ANAHTARI[str(st.session_state.soru_no)].lower()
    
    # Esnek kontrol (Tahmin doğru cevabın içinde geçiyorsa)
    if tahmin in dogru_cevap and len(tahmin) > 2:
        st.session_state.durum = "dogru"
    else:
        st.session_state.durum = "yanlis"

def sonraki():
    if st.session_state.soru_no < 24:
        st.session_state.soru_no += 1
    else:
        st.session_state.soru_no = 1 # Başa dön
    st.session_state.durum = None
    st.session_state.tahmin_input = ""

# --- ARAYÜZ ---
st.title("⚡ Pano Elemanlarını Tanıyalım")
st.write(f"### Soru: {st.session_state.soru_no} / 24")

# Resim Yükleme Mantığı
resim_adi = f"{st.session_state.soru_no}.jpg" # Dosya uzantın .png ise burayı .png yap
resim_yolu = os.path.join(KLASOR_ADI, resim_adi)

if os.path.exists(resim_yolu):
    img = Image.open(resim_yolu)
    st.image(img, use_container_width=True, caption=f"Görsel No: {resim_adi}")
    
    st.text_input("Bu elemanın adı nedir?", key="tahmin_input", on_change=kontrol)
    
    if st.session_state.durum == "dogru":
        st.success(f"TEBRİKLER! ✅ Doğru Cevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Sonraki Eleman ➡️", on_click=sonraki)
        
    elif st.session_state.durum == "yanlis":
        st.error(f"YANLIŞ! ❌ Doğru Cevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Sıradakine Geç ➡️", on_click=sonraki)
else:
    st.error(f"Hata: '{resim_yolu}' dosyası bulunamadı. Lütfen '{KLASOR_ADI}' klasöründe 1.jpg, 2.jpg... şeklinde resimlerin olduğundan emin ol.")
