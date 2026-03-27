import streamlit as st
import google.generativeai as genai
import datetime

# הגדרת המפתח מתוך ה-Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Missing API Key in Secrets")
except Exception as e:
    st.error(f"Connection Error: {e}")

# הגדרות עמוד ועיצוב RTL
st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Assistant', sans-serif;
        background-color: #050a0e;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] { direction: RTL; gap: 10px; }
    h1, h2, h3, p, span, label { text-align: right !important; direction: RTL !important; }
    .stButton>button {
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: black !important;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
    }
    .stSlider { direction: LTR !important; }
    div[role="radiogroup"] { direction: RTL !important; }
    </style>
    """, unsafe_allow_html=True)

def safe_generate(prompt_content):
    try:
        response = model.generate_content(prompt_content)
        return response.text
    except Exception as e:
        return f"שגיאה: {e}"

st.title("⚡ BodyTrack AI Pro")

# בחירת מגדר גלובלית שתשפיע על הכל
gender = st.sidebar.radio("מין:", ["גבר", "אישה"])
st.sidebar.divider()
st.sidebar.info(f"התוכנית תותאם ל{gender}")

tab1, tab2, tab3, tab4 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים", "✅ יומן ניצחונות"])

with tab1:
    st.header("בניית תוכנית אימון")
    location = st.radio("איפה מתאמנים?", ["חדר כושר", "בית (משקל גוף)", "פארק / גינת כושר"])
    goal = st.selectbox("מה המטרה?", ["בניית מסת שריר", "חיטוב אגרסיבי", "כוח מתפרץ"])
    days = st.slider("כמה ימים בשבוע?", 1, 7, 3)
    
    if st.button("בנה לי תוכנית אימון"):
        with st.spinner('מעבד נתונים...'):
            prompt = f"צור תוכנית אימון ל{gender} למטרת {goal} ב{location} למשך {days} ימים בשבוע. כתוב בעברית."
            st.markdown(safe_generate(prompt))

with tab2:
    st.header("🥗 תפריט תזונה")
    target = st.selectbox("בחר יעד תזונתי:", ["מסה", "חיטוב", "תחזוקה"])
    
    if st.button("צור תפריט יומי"):
        with st.spinner('מחשב קלוריות...'):
            prompt = f"צור תפריט יומי ל{gender} למטרת {target}. תתחשב בצרכים הקלוריים של {gender}. עברית."
            st.success(safe_generate(prompt))

with tab3:
    st.header("📊 מחשבון BMI")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input('משקל (ק"ג)', 30.0, 200.0, 70.0)
    with col2:
        height = st.number_input('גובה (ס"מ)', 100, 250, 180)
    
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")

with tab4:
    st.header("📝 יומן ניצחונות")
    st.subheader(f"סטטוס להיום: {datetime.date.today().strftime('%d/%m/%Y')}")
    c1, c2 = st.columns(2)
    with c1:
        w_done = st.checkbox("אימון: בוצע! 🏋️")
    with c2:
        f_done = st.checkbox("תזונה: אכלתי נכון! 🍱")
    
    if w_done and f_done:
        st.balloons()
        st.success("אלוף! יום מושלם.")
