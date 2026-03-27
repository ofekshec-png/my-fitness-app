import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import time

# הגדרת המפתח מתוך ה-Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        # שימוש בשם מודל פשוט ללא קידומות models/
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("המפתח GOOGLE_API_KEY חסר ב-Secrets.")
except Exception as e:
    st.error(f"שגיאה בחיבור: {e}")

st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

# עיצוב RTL ורקע
st.markdown("""
    <style>
    .main, .stApp {
        direction: RTL;
        text-align: right;
        background: linear-gradient(135deg, #020202, #05141e, #020202);
        background-size: 300% 300%;
        animation: breathingGradient 15s ease infinite;
    }
    @keyframes breathingGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    h1 { color: #00ff88; text-shadow: 0px 0px 15px rgba(0, 255, 136, 0.5); }
    .stButton>button { background: #00ff88 !important; color: black !important; font-weight: bold !important; border-radius: 12px; }
    .stSlider [data-baseweb="slider"] { direction: LTR; }
    </style>
    """, unsafe_allow_html=True)

def safe_generate(prompt_content):
    try:
        # פנייה ישירה למודל
        response = model.generate_content(prompt_content)
        return response.text
    except Exception as e:
        return f"שגיאה: {e}"

st.title("⚡ BodyTrack AI Pro")
tab1, tab2 = st.tabs(["🏋️ תוכנית אימון", "📊 מדדים"])

with tab1:
    st.header("⚡ תוכנית אימון אישית")
    goal = st.selectbox("מטרה:", ["בניית שריר", "חיטוב אגרסיבי", "כוח"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    if st.button("בנה תוכנית"):
        with st.spinner('יוצר תוכנית...'):
            res = safe_generate(f"Create a {goal} workout for {days} days in Hebrew.")
            st.markdown(res)

with tab2:
    w = st.number_input("משקל (kg)", 30, 200, 70)
    st.write(f"המשקל שהוזן: {w}")
