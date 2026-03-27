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
        
        # שיטת המעקף: הגדרת המודל עם שם מפורש וגרסה
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
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
    .stButton>button { 
        background-color: #00ff88 !important; 
        color: black !important; 
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] { direction: RTL; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BodyTrack AI Pro")

tab1, tab2, tab3 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים"])

with tab1:
    st.header("בניית תוכנית אימון")
    goal = st.selectbox("מטרה:", ["בניית שריר", "חיטוב", "כוח"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    
    if st.button("בנה לי תוכנית"):
        with st.spinner('ה-AI חושב...'):
            try:
                # כאן אנחנו מנסים לייצר תוכן
                response = model.generate_content(f"צור תוכנית אימון ל{goal} למשך {days} ימים בשבוע. עברית.")
                st.write(response.text)
            except Exception as e:
                # אם עדיין יש שגיאה, נציג אותה בצורה ברורה
                st.error(f"שגיאה בייצור התוכן: {e}")

with tab2:
    st.header("ניתוח תזונה")
    st.info("כאן תוכל להזין מה אכלת היום")

with tab3:
    st.header("מחשבון BMI")
    weight = st.number_input("משקל בק"ג", 30, 200, 70)
    height = st.number_input("גובה בס"מ", 100, 250, 180)
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", round(bmi, 1))
