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
        # שימוש בשם המודל המדויק לגרסה החדשה
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Missing API Key in Secrets")
except Exception as e:
    st.error(f"Connection Error: {e}")

st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

# עיצוב RTL, רקע נושם וכפתורי ניאון
st.markdown("""
    <style>
    .main, .stApp {
        direction: RTL;
        text-align: right;
        background-color: #050a0e;
        color: white;
    }
    h1 { color: #00ff88; font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { direction: RTL; gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 31, 36, 0.8);
        border-radius: 10px 10px 0px 0px;
        color: white;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ff88 !important;
        color: black !important;
        font-weight: bold;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: black !important; 
        font-weight: bold;
        border-radius: 12px;
        border: none;
        width: 100%;
    }
    
    /* תיקון הסליידר - מכריחים אותו ליישור לשמאל כדי שלא יברח מהטווח */
    .stSlider [data-baseweb="slider"] {
        direction: LTR !important;
        text-align: left !important;
        margin-left: 20px !important;
        margin-right: 0 !important;
        width: 95% !important;
    }
    /* תיקון צבע הכיתוב על הסליידר שיהיה קריא */
    .stSlider p { color: white !important; }
    
    /* תיקון צבע פונט בתיבת הבחירה */
    .stSelectbox label { color: white; }
    .stSelectbox > div { background-color: rgba(26, 31, 36, 0.8); }
    /* תיקון צבע פונט בכפתורי הרדיו */
    .stRadio label { color: white; }
    </style>
    """, unsafe_allow_html=True)

# פונקציית ייצור תוכן עם טיפול בשגיאות
def safe_generate(prompt_content):
    try:
        response = model.generate_content(prompt_content)
        if response and response.text:
            return response.text
        return "לא התקבלה תשובה מהמודל."
    except Exception as e:
        if "429" in str(e):
            time.sleep(2)
            try:
                response = model.generate_content(prompt_content)
                return response.text
            except:
                return "עומס כבד בשרתי גוגל. נסה שוב בעוד דקה."
        return f"שגיאה בייצור התוכן: {e}"

st.title("⚡ BodyTrack AI Pro")
tab1, tab2, tab3 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים"])

with tab1:
    st.header("בניית תוכנית אימון אישית")
    location = st.radio("מיקום:", ["חדר כושר", "בית (משקל גוף)", "פארק"])
    goal = st.selectbox("מטרה עיקרית:", ["בניית שריר (Hypertrophy)", "חיטוב אגרסיבי", "כוח מתפרץ"])
    # הסליידר המתוקן
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    
    if st.button("בנה לי תוכנית"):
        with st.spinner('ה-AI חושב על אימונים...'):
            res_text = safe_generate(f"Workout plan for {goal} at {location} for {days} days. Hebrew.")
            if "שגיאה" in res_text:
                st.error(res_text)
            else:
                st.markdown(res_text)

with tab2:
    st.header("🥗 תפריט מותאם")
    target = st.selectbox("מה המטרה התזונתית שלך?", ["מסה נקייה", "חיטוב אגרסיבי"])
    if st.button("צור תפריט עכשיו"):
        with st.spinner('בונה תפריט...'):
            res_text = safe_generate(f"צור תפריט יומי ל{target} עם חלבון גבוה. ענה בעברית.")
            if "שגיאה" in res_text:
                st.error(res_text)
            else:
                st.success(res_text)

with tab3:
    st.header("📊 מחשבון מדדים")
    weight = st.number_input('משקלבק"ג', 30.0, 200.0, 70.0)
    height = st.number_input('גובה בס"מ', 100, 250, 180)
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")
        if bmi < 18.5: st.warning("תת משקל. צריך לאכול!")
        elif bmi < 25: st.success("תקין! כל הכבוד.")
        else: st.info("עודף משקל. זמן לחיטוב.")
