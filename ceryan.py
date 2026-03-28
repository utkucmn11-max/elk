import streamlit as st
import os
import random
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Pano Elemanları Sınavı", page_icon="⚡", layout="wide")

# --- MEVCUT DİZİN ---
base_path = os.path.dirname(__file__)

# --- CEVAP ANAHTARI ---
CEVAP_ANAHTARI = {
    "1": "Bir fazlı sigorta", "2": "Üç fazlı sigorta", "3": "NH bıçaklı sigorta",
    "4": "Kaçak akım rölesi", "5": "Üç fazlı paket şalter", "6": "Termik manyetik şalter",
    "7": "Akım transformatörü", "8": "Bir fazlı aktif sayaç", "9": "Üç fazlı aktif sayaç",
    "10": "Üç fazlı kombi sayaç", "11": "Ampermetre voltmetre", "12": "Ray klemensi",
    "13": "Sinyal lambası", "14": "Start butonu", "15": "Stop butonu",
    "16": "Jog buton", "17": "Aşırı akım rölesi", "18": "Motor koruma şalteri",
    "19": "Kontaktör", "20": "Zaman rölesi", "21": "Motor koruma rölesi",
    "22": "Faz sırası rölesi", "23": "Kondansatör", "24": "Alçak gerilim parafudr"
}

# --- DURUM YÖNETİMİ ---
if 'soru_sirasi' not in st.session_state:
    liste = list(range(1, 25))
    random.shuffle(liste)
    st.session_state.soru_sirasi = liste
    st.session_state.liste_index = 0
    st.session_state.puan = 0

if 'durum' not in st.session_state:
    st.session_state.durum = None

def normalize_text(text):
    text = text.replace('İ', 'i').replace('I', 'ı').lower()
    mapping = str.maketrans("çğışıöü", "cgisiou")
    return text.translate(mapping).strip()

def kontrol():
    if not st.session_state.tahmin_input:
        return
    no = st.session_state.soru_sirasi[st.session_state.liste_index]
    tahmin = normalize_text(st.session_state.tahmin_input)
    gercek = normalize_text(CEVAP_ANAHTARI[str(no)])
    
    if (tahmin in gercek or gercek in tahmin) and len(tahmin) >= 3:
        st.session_state.durum = "dogru"
        st.session_state.puan += 5
    else:
        st.session_state.durum = "yanlis"

def sonraki():
    st.session_state.liste_index += 1
    if st.session_state.liste_index >= 24:
        random.shuffle(st.session_state.soru_sirasi)
        st.session_state.liste_index = 0
    st.session_state.durum = None
    st.session_state.tahmin_input = ""

# --- ARAYÜZ ---
st.title("🛡️ Elektrik Pano Elemanları Eğitim Portalı")
st.markdown(f"**Puan:** `{st.session_state.puan}` | **Soru:** `{st.session_state.liste_index + 1} / 24`")
st.divider()

aktif_no = st.session_state.soru_sirasi[st.session_state.liste_index]
img_path = os.path.join(base_path, f"{aktif_no}.jpg")

# Sütunları dengeleyelim
col_resim, col_input = st.columns([1.6, 1], gap="large")

with col_resim:
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, use_container_width=True, caption=f"Eleman No: {aktif_no}")
    else:
        st.error(f"Görsel bulunamadı: {aktif_no}.jpg")

with col_input:
    # Görselin yanına dikeyde ortalamak için boşluk
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.subheader("Bu elemanın adı nedir?")
    # Cevap kutucuğu
    st.text_input("Tahmininizi yazın:", key="tahmin_input", placeholder="Örn: Kontaktör", label_visibility="collapsed")
    
    # Onaylama Butonu (Cevap verilmediyse gösterilir)
    if st.session_state.durum is None:
        st.button("✅ Cevabı Onayla", on_click=kontrol, use_container_width=True)

    # Sonuç Ekranı ve Sonraki Butonu
    if st.session_state.durum == "dogru":
        st.success(f"### DOĞRU! ✅\n**{CEVAP_ANAHTARI[str(aktif_no)]}**")
        st.button("Sıradaki Soru ➡️", on_click=sonraki, use_container_width=True)
        st.balloons()
        
    elif st.session_state.durum == "yanlis":
        st.error(f"### YANLIŞ! ❌\nDoğru Cevap: **{CEVAP_ANAHTARI[str(aktif_no)]}**")
        st.button("Devam Et ➡️", on_click=sonraki, use_container_width=True)

st.divider()
if st.sidebar.button("🔄 Testi Sıfırla"):
    del st.session_state.soru_sirasi
    st.session_state.puan = 0
    st.rerun()
