import streamlit as st

# Sayfa yapılandırması
st.set_page_config(page_title="Pano Elemanları Bilgi Yarışması", layout="centered")

# Sabit veri seti (Görsel URL'leri ve Doğru Cevaplar)
# Not: Buradaki URL'leri gerçek görsellerle değiştirmelisin.
QUESTIONS = [
    {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Miniature_circuit_breaker_2_pole.jpg/800px-Miniature_circuit_breaker_2_pole.jpg",
        "answer": "sigorta",
        "hint": "Devreyi aşırı akımdan korur."
    },
    {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Contactor_3_phase.jpg/800px-Contactor_3_phase.jpg",
        "answer": "kontaktör",
        "hint": "Büyük güçteki elektrik devrelerini anahtarlamak için kullanılır."
    },
    {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Thermal_overload_relay.jpg/800px-Thermal_overload_relay.jpg",
        "answer": "termik röle",
        "hint": "Motorları aşırı ısınmaya karşı korur."
    }
]

# Session State (Oturum Durumu) Yönetimi
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'result' not in st.session_state:
    st.session_state.result = None

def check_answer():
    user_answer = st.session_state.user_input.lower().strip()
    correct_answer = QUESTIONS[st.session_state.current_step]['answer']
    
    if user_answer == correct_answer:
        st.session_state.result = "correct"
    else:
        st.session_state.result = "wrong"

def next_question():
    st.session_state.current_step = (st.session_state.current_step + 1) % len(QUESTIONS)
    st.session_state.result = None
    st.session_state.user_input = ""

# Arayüz Başlığı
st.title("⚡ Pano Elemanlarını Tanı!")
st.write(f"Soru: {st.session_state.current_step + 1} / {len(QUESTIONS)}")

# Görseli Göster
current_q = QUESTIONS[st.session_state.current_step]
st.image(current_q['image'], caption="Bu eleman nedir?", use_container_width=True)

# Girdi Alanı
st.text_input("Tahminini buraya yaz:", key="user_input", on_change=check_answer)

# Sonuç Kontrolü ve Renkli Geri Bildirim
if st.session_state.result == "correct":
    st.success(f"DOĞRU! ✅ Bu bir: **{current_q['answer'].upper()}**")
    st.balloons()
    st.button("Sonraki Elemana Geç ➡️", on_click=next_question)

elif st.session_state.result == "wrong":
    st.error(f"YANLIŞ! ❌ Doğru cevap: **{current_q['answer'].upper()}**")
    st.button("Sonraki Elemana Geç ➡️", on_click=next_question)

# Alt Bilgi
st.info(f"İpucu: {current_q['hint']}")