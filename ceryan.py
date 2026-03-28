import streamlit as st
import os
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Pano Elemanı Testi", page_icon="⚙️")

# --- CEVAP ANAHTARI (Tablodaki Sıraya Göre) ---
# Eğer resim sıran farklıysa buradaki isimlerin yerini değiştirebilirsin.
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
    "11": "Ampermetre voltmetre",
    "12": "Ray klemensi",
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

KLASOR_ADI = "yeni klasör"

if 'soru_no' not in st.session_state:
    st.session_state.soru_no = 1
if 'durum' not in st.session_state:
    st.session_state.durum = None

def kontrol():
    tahmin = st.session_state.tahmin_input.lower().strip()
    dogru_cevap = CEVAP_ANAHTARI[str(st.session_state.soru_no)].lower()
    
    # Esnek kontrol: Tahmin cevabın içinde geçiyorsa doğru say
    if tahmin in dogru_cevap and len(tahmin) > 2:
        st.session_state.durum = "dogru"
    else:
        st.session_state.durum = "yanlis"

def sonraki():
    st.session_state.soru_no = (st.session_state.soru_no % 24) + 1
    st.session_state.durum = None
    st.session_state.tahmin_input = ""

# --- ARAYÜZ ---
st.title("⚡ Pano Elemanlarını Tanıyalım")
st.write(f"### Soru: {st.session_state.soru_no} / 24")

# Dosya adını (1).png formatında oluşturuyoruz
resim_adi = f"({st.session_state.soru_no}).png"
resim_yolu = os.path.join(KLASOR_ADI, resim_adi)

col1, col2 = st.columns([1, 1])

with col1:
    if os.path.exists(resim_yolu):
        img = Image.open(resim_yolu)
        st.image(img, use_container_width=True, caption=f"Dosya: {resim_adi}")
    else:
        st.error(f"⚠️ Hata: '{resim_yolu}' dosyası bulunamadı!")
        st.info("Lütfen 'yeni klasör' içinde resimlerin (1).png, (2).png... şeklinde olduğundan emin ol.")

with col2:
    st.text_input("Bu hangi pano elemanı?", key="tahmin_input", on_change=kontrol)
    
    if st.session_state.durum == "dogru":
        st.success(f"DOĞRU! ✅\n\nCevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Sonraki ➡️", on_click=sonraki)
        
    elif st.session_state.durum == "yanlis":
        st.error(f"YANLIŞ! ❌\n\nDoğru cevap: **{CEVAP_ANAHTARI[str(st.session_state.soru_no)]}**")
        st.button("Atla ➡️", on_click=sonraki)

st.divider()
