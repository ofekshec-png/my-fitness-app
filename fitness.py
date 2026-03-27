import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import time
import random

# הגדרת המפתח מתוך ה-Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        # תיקון השם לפורמט המלא כדי למנוע שגיאת 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    else:
        st.error("המפתח GOOGLE_API_KEY חסר ב-Secrets.")
except Exception as e:
    st.error(f"שגיאה בחיבור ל-AI: {e}")

st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

# עיצוב מתקדם: רקע נושם ויישור לימין
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
    h1 { color: #00ff88; text-shadow: 0px 0px 15px rgba(0, 255, 136, 0.5); font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(26, 31, 36, 0.8); border-radius: 10px 10px 0px 0px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00ff88 !important; color: #050a0e !important; }
    div.stButton > button { background: linear-gradient(90deg, #00ff88, #00cc66); color: #050a0e !important; font-weight: bold; border-radius: 12px; border: none; }
    .stSlider [data-baseweb="slider"] { direction: LTR; margin-top: 25px; }
    .stNumberInput, .stTextInput, .stSelectbox { background-color: rgba(26, 31, 36, 0.8); border-radius: 8px; }
    
    /* תיקון צבע טקסט בכפתורים שיהיה שחור קריא */
    .stButton>button { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# פונקציה חכמה למניעת עומס (Retries)
def safe_generate(prompt_content):
    try:
        response = model.generate_content(prompt_content)
        return response.text
    except Exception as e:
        if "429" in str(e):
            time.sleep(2)
            try:
                response = model.generate_content(prompt_content)
                return response.text
            except:
                return "השרת של גוגל עמוס כרגע. נסה שוב בעוד דקה."
        return f"שגיאה בייצור תוכן: {e}"

st.title("⚡ BodyTrack AI Pro")
tab1, tab2, tab3, tab4 = st.tabs(["📸 סורק ארוחות", "🏋️ תוכניות אימון", "📊 מדדים", "📝 יומן"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("🔍 ניתוח ארוחה")
        uploaded_file = st.file_uploader("העלה תמונה", type=["jpg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            if st.button("נתח ערכים"):
                with st.spinner('מנתח...'):
                    res_text = safe_generate(["Analyze this meal. Calories, Protein, Carbs, Fats. Hebrew.", image])
                    st.info(res_text)
    with col2:
        st.header("🥗 תפריט מותאם")
        target = st.selectbox("מטרה:", ["מסה נקייה", "מסה מלוכלכת", "חיטוב אגרסיבי"])
        if st.button("צור תפריט"):
            with st.spinner('בונה תפריט...'):
                res_text = safe_generate(f"צור תפריט יומי ל{target} עם דגש על חלבון גבוה. עברית.")
                st.success(res_text)

with tab2:
    st.header("⚡ תוכנית אימון")
    c_a, c_b = st.columns(2)
    with c_a: loc = st.radio("מיקום:", ["חדר כושר", "בית", "פארק"])
    with c_b: goal = st.selectbox("מטרה:", ["בניית שריר", "כוח", "סיבולת", "חיטוב אגרסיבי"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    if st.button("בנה תוכנית"):
        with st.spinner('מעבד...'):
            res_text = safe_generate(f"Workout plan for {goal} at {loc} for {days} days. Hebrew.")
            st.markdown(res_text)

with tab3:
    st.header("📊 מחשבון")
    w = st.number_input("משקל (kg)", 30.0, 200.0, 60.0)
    h = st.number_input("גובה (cm)", 100, 250, 180)
    if h > 0:
        bmi = w / ((h/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")

with tab4:
    st.header("📝 יומן")
    st.write(f"היום: {datetime.date.today()}")
    workout_done = st.checkbox("סיימתי אימון היום! ✅")
    if workout_done:
        st.balloons()
        st.success("כל הכבוד אלוף!")
