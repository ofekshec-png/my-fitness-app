import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import time

# הגדרת המפתח
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        # תיקון השגיאה - שם המודל ללא קידומת models/
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Missing API Key in Secrets")
except Exception as e:
    st.error(f"Connection Error: {e}")

# עיצוב האפליקציה (RTL וצבעים)
st.markdown("""
    <style>
    .main, .stApp {
        direction: RTL;
        text-align: right;
        background-color: #050a0e;
        color: white;
    }
    h1 { color: #00ff88; }
    .stTabs [data-baseweb="tab-list"] { 
        direction: RTL; 
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 31, 36, 0.8);
        border-radius: 8px;
        color: white;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ff88 !important;
        color: black !important;
        font-weight: bold;
    }
    .stButton>button { 
        background-color: #00ff88 !important; 
        color: black !important; 
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    /* תיקון צבע פונט בתיבת הבחירה */
    .stSelectbox label { color: white; }
    .stSelectbox > div { background-color: rgba(26, 31, 36, 0.8); }
    /* תיקון צבע פונט בכפתורי הרדיו */
    .stRadio label { color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BodyTrack AI Pro")

tab1, tab2, tab3 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים"])

with tab1:
    st.header("בניית תוכנית אימון")
    location = st.radio("מיקום:", ["חדר כושר", "בית (משקל גוף)", "פארק"])
    goal = st.selectbox("מטרה:", ["בניית שריר", "חיטוב אגרסיבי", "כוח מתפרץ"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    
    if st.button("בנה לי תוכנית"):
        with st.spinner('ה-AI חושב על אימונים...'):
            try:
                response = model.generate_content(f"צור תוכנית אימון ל{goal} ב{location} למשך {days} ימים בשבוע. עברית.")
                st.write(response.text)
            except Exception as e:
                st.error(f"שגיאה בייצור התוכן: {e}")

with tab2:
    st.header("🥗 תפריט מותאם")
    target = st.selectbox("מה המטרה שלך?", ["מסה נקייה", "חיטוב אגרסיבי"])
    if st.button("צור תפריט עכשיו"):
        with st.spinner('בונה תפריט...'):
            try:
                response = model.generate_content(f"צור תפריט יומי ל{target} עם חלבון גבוה. עברית.")
                st.success(response.text)
            except Exception as e:
                st.error(f"גוגל עמוסה. {e}")

with tab3:
    st.header("📊 מחשבון מדדים")
    # תיקון השגיאה: שימוש בגרשיים בודדים
    weight = st.number_input('משקל בק"ג', 30, 200, 70)
    height = st.number_input('גובה בס"מ', 100, 250, 180)
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", round(bmi, 1))
        if bmi < 18.5: st.warning("תת משקל. צריך לאכול!")
        elif bmi < 25: st.success("תקין! כל הכבוד.")
        else: st.info("עודף משקל. זמן לחיטוב.")
