import streamlit as st
import os
import random
from PIL import Image

# Sayfa Ayarları
st.set_page_config(page_title="Pano Elemanı Karma Test", page_icon="🎲", layout="wide")

# --- MEVCUT DİZİN AYARI ---
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

# --- KARMA MANTIĞI (Sadece bir kez çalışır) ---
if 'soru_sirasi' not in st.session_state:
    # 1'den 24'e kadar sayıları al ve karıştır
    liste = list(range(1, 25))
    random.shuffle(liste)
    st.session_state.soru_sirasi = liste
    st.session_state.liste_index = 0 # Listenin kaçıncı elemanındayız?

if 'durum' not in st.session_state:
    st.session_state.durum = None

# --- GELİŞMİŞ KARAKTER NORMALİZASYONU ---
def normalize_text(text):
    text = text.replace('İ', 'i').replace('I', 'ı').lower()
    mapping = str.maketrans("çğışıöü", "cgisiou")
    return text.translate(mapping).strip()

def kontrol():
    if not st.session_state.tahmin_input:
        return
    # Mevcut sorunun numarasını bul (Karıştırılmış listeden çek)
    su_anki_no = st.session_state.soru_sirasi[st.session_state.liste_index]
    user_guess = normalize_text(st.session_state.tahmin_input)
    correct_answer = normalize_text(CEVAP_ANAHTARI[str(su_anki_no)])
    
    if (user_guess in correct_answer or correct_answer in user_guess) and len(user_guess) >= 3:
        st.session_state.durum = "dogru"
    else:
        st.session_state.durum = "yanlis"

def sonraki():
    # Bir sonraki karıştırılmış soruya geç
    st.session_state.liste_index += 1
    
    # Eğer 24 soru bittiyse listeyi yeniden karıştır ve başa dön
    if st.session_state.liste_index >= 24:
        random.shuffle(st.session_state.soru_sirasi)
        st.session_state.liste_index = 0
        st.toast("Tebrikler! Tüm soruları bitirdin, liste yeniden karıştırıldı.", icon="🎉")
        
    st.session_state.durum = None
    st.session_state.tahmin_input = ""

# --- ARAYÜZ ---
st.title("🛡️ Pano Elemanları - Karışık Sınav Modu")
st.divider()

# Karıştırılmış listeden şu anki görsel numarasını al
aktif_resim_no = st.session_state.soru_sirasi[st.session_state.liste_index]
resim_adi = f"{aktif_resim_no}.jpg"
image_path = os.path.join(base_path, resim_adi)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown(f"<h1 style='text-align: center; color: #ff4b4b;'>Soru: {st.session_state.liste_index + 1} / 24</h1>", unsafe_allow_html=True)
    
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, use_column_width=True)
    else:
        st.error(f"⚠️ Dosya bulunamadı: {resim_adi}")

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Tahmininiz:")
    st.text_input("", key="tahmin_input", on_change=kontrol, placeholder="Cevabı buraya yazın...")
    
    if st.session_state.durum == "dogru":
        st.success(f"### DOĞRU! ✅\n\nCevap: **{CEVAP_ANAHTARI[str(aktif_resim_no)]}**")
        st.button("Sıradaki (Rastgele) ➡️", on_click=sonraki)
        st.balloons()
        
    elif st.session_state.durum == "yanlis":
        st.error(f"### YANLIŞ! ❌\n\nDoğru Cevap: **{CEVAP_ANAHTARI[str(aktif_resim_no)]}**")
        st.button("Atla ve Devam Et ➡️", on_click=sonraki)

st.divider()
if st.button("Listeyi Şimdi Yeniden Karıştır 🔄"):
    del st.session_state.soru_sirasi
    st.rerun()
