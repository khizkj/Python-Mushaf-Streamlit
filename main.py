import streamlit as st
import requests

st.set_page_config(page_title="MushafWebApp", page_icon="📖", layout="wide")


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Amiri&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #101820, #1E2A38);
        color: #fff;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #fff;
        font-weight: 700;
        text-shadow: 0 0 10px #00c3ff;
        margin-bottom: 30px;
    }
    .ayah-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        margin-bottom: 18px;
        transition: 0.3s ease;
    }
    .ayah-card:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 16px rgba(0,0,0,0.6);
    }
    .ayah-text {
        text-align: right;
        font-size: 1.6rem;
        color: #fafafa;
        direction: rtl;
        font-family: 'Amiri', serif;
        line-height: 2.3rem;
        font-weight: 500;
    }
    .translation-box {
        margin-top: 10px;
        font-size: 1.1rem;
        background: rgba(0,195,255,0.1);
        border-left: 4px solid #00c3ff;
        padding: 10px 15px;
        border-radius: 10px;
    }
    .footer {
        text-align: center;
        color: #bbb;
        font-size: 0.9rem;
        margin-top: 40px;
    }
    [data-testid="stSidebar"] {
        background: #101820;
        color: #eee;
    }
    .css-1d391kg, .css-1v0mbdj {
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📖 Mushaf Practice App</h1>", unsafe_allow_html=True)


st.sidebar.title("⚙️ Controls")
st.sidebar.markdown("Customize your reading experience:")

surahlist = requests.get("https://api.alquran.cloud/v1/surah").json()["data"]
surah_names = [f"{surah['number']}. {surah['englishName']} ({surah['name']})" for surah in surahlist]
selected_surah_name = st.sidebar.selectbox('📚 Select Surah', surah_names)
selected_surah_num = int(selected_surah_name.split('.')[0])

search_keyword = st.sidebar.text_input("Search Arabic Ayah")
show_translation = st.sidebar.checkbox("Show Translation")
show_recitation = st.sidebar.checkbox("🎧 Play Recitation")
choice_tr = st.sidebar.selectbox("Select Translation", ["en.asad", "ur.maududi", "en.sahih", "en.yusufali"])


recitation_url = f"https://api.alquran.cloud/v1/surah/{selected_surah_num}/ar.abdurrahmaansudais"
rec_response = requests.get(recitation_url).json()
arabic_ayah = rec_response["data"]["ayahs"]

if show_translation:
    translation_url = f"https://api.alquran.cloud/v1/surah/{selected_surah_num}/{choice_tr}"
    tr_response = requests.get(translation_url).json()
    tr_ayah = tr_response["data"]["ayahs"]
else:
    tr_ayah = [None] * len(arabic_ayah)

if search_keyword.strip():
    filtered_ar, filtered_tr = [], []
    for i, ayah in enumerate(arabic_ayah):
        if search_keyword in ayah["text"]:
            filtered_ar.append(ayah)
            filtered_tr.append(tr_ayah[i])
    arabic_ayah, tr_ayah = filtered_ar, filtered_tr

st.subheader(f"📖 {selected_surah_name}")
for i, ayah in enumerate(arabic_ayah):
    st.markdown(f"<div class='ayah-card'><div class='ayah-text'>﴿{ayah['text']}﴾</div>", unsafe_allow_html=True)
    if show_recitation and 'audio' in ayah and ayah["audio"]:
        st.audio(ayah['audio'], format="audio/mp3")
    if show_translation and tr_ayah[i]:
        st.markdown(f"<div class='translation-box'>{tr_ayah[i]['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>✨ Developed by <b>Khizer Jamil</b></div>", unsafe_allow_html=True)
