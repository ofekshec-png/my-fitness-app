import streamlit as st
import google.generativeai as genai
import datetime

# התחברות לגוגל דרך ה-Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        # שימוש בשם המודל הכי עדכני ויציב
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    else:
        st.error("Missing API Key in Secrets")
except Exception as e:
    st.error(f"Connection Error: {e}")

st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

# עיצוב מושלם כולל פתרון לסליידר
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
    }
    .stTabs [aria-selected="true"] { background-color: #00ff88 !important; color: black !important; }
    .stButton>button { 
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: black !important; 
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
    }
    .stSlider [data-baseweb="slider"] { direction: LTR !important; }
    .stCheckbox label p { font-size: 1.2rem; font-weight: bold; color: #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# פונקציית יצירת תוכן שחושפת שגיאות אמיתיות אם יש
def safe_generate(prompt_content):
    try:
        response = model.generate_content(prompt_content)
        return response.text
    except Exception as e1:
        try:
            # מודל גיבוי
            alt_model = genai.GenerativeModel('gemini-pro')
            response = alt_model.generate_content(prompt_content)
            return response.text
        except Exception as e2:
            return f"שגיאה מערכתית. עדכן גרסאות ב-requirements. \nשגיאה 1: {e1} \nשגיאה 2: {e2}"

st.title("⚡ BodyTrack AI Pro")
tab1, tab2, tab3, tab4 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים", "✅ יומן ניצחונות"])

with tab1:
    st.header("בניית תוכנית אימון")
    location = st.radio("מיקום:", ["חדר כושר", "בית (משקל גוף)", "פארק"])
    goal = st.selectbox("מטרה עיקרית:", ["בניית שריר", "חיטוב אגרסיבי", "כוח מתפרץ"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    
    if st.button("בנה לי תוכנית"):
        with st.spinner('ה-AI חושב...'):
            st.markdown(safe_generate(f"Create a workout plan for {goal} at {location} for {days} days. Hebrew."))

with tab2:
    st.header("🥗 תפריט מותאם")
    target = st.selectbox("מטרה תזונתית:", ["מסה", "חיטוב"])
    if st.button("צור תפריט עכשיו"):
        with st.spinner('בונה תפריט...'):
            st.success(safe_generate(f"צור תפריט יומי ל{target} עם חלבון גבוה. עברית."))

with tab3:
    st.header("📊 מחשבון מדדים")
    weight = st.number_input('משקל בק"ג', 30.0, 200.0, 70.0)
    height = st.number_input('גובה בס"מ', 100, 250, 180)
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")

with tab4:
    st.header("📝 המעקב היומי שלי")
    st.subheader(f"תאריך: {datetime.date.today().strftime('%d/%m/%Y')}")
    c1, c2 = st.columns(2)
    with c1:
        workout = st.checkbox("סימון אימון: נתתי בראש! 🏋️")
    with c2:
        food = st.checkbox("סימון תזונה: שמרתי על התפריט! 🍱")
    
    if workout and food:
        st.balloons()
        st.success("אלוף! סגרת יום מושלם בדרך למטרה.")
