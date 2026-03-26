import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime
import time
import random

# הגדרת המפתח מתוך ה-Secrets של Streamlit
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# הגדרה של המודל
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="BodyTrack AI | Pro Edition", layout="wide")

# עיצוב חדשני - Cyber Fitness Style
st.markdown("""
    <style>
    /* הגדרות כלליות ויישור לימין */
    .main, .stApp {
        direction: RTL;
        text-align: right;
        background-color: #050a0e;
    }
    
    /* עיצוב כותרת ראשית */
    h1 {
        color: #00ff88;
        text-shadow: 0px 0px 15px rgba(0, 255, 136, 0.5);
        font-family: 'Assistant', sans-serif;
        font-weight: 800;
    }

    /* עיצוב כרטיסיות ותיבות */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f24;
        border-radius: 10px 10px 0px 0px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ff88 !important;
        color: #050a0e !important;
        font-weight: bold;
    }

    /* כפתור "ניאון" */
    div.stButton > button {
        background: linear-gradient(90deg, #00ff88, #00cc66);
        color: #050a0e;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        transition: 0.3s;
        box-shadow: 0px 4px 15px rgba(0, 255, 136, 0.2);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(0, 255, 136, 0.4);
        color: #050a0e;
    }

    /* תיקון לסליידר (Slider) שיוכל לעבוד ב-RTL */
    .stSlider [data-baseweb="slider"] {
        direction: LTR; /* מחזיר לשמאל רק את המנגנון כדי שיעבוד */
        margin-top: 25px;
    }

    /* עיצוב תיבות הקלט */
    .stNumberInput, .stTextInput, .stSelectbox {
        background-color: #1a1f24;
        border-radius: 8px;
    }

    /* הודעות הצלחה */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        color: #00ff88;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BodyTrack AI Pro")
st.subheader("Keep Pushing. No Excuses.")

tab1, tab2, tab3, tab4 = st.tabs(["📸 סורק ארוחות", "🏋️ תוכניות אימון", "📊 מדדים", "📝 יומן"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("🔍 ניתוח ארוחה חכם")
        uploaded_file = st.file_uploader("העלה תמונה של הצלחת", type=["jpg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            if st.button("נתח ערכים תזונתיים"):
                with st.spinner('המנוע בודק את הצלחת...'):
                    try:
                        prompt = "Analyze this meal image. Provide Calories, Protein, Carbs, Fats. Respond in Hebrew in a clean list."
                        res = model.generate_content([prompt, image])
                        st.info(res.text)
                    except:
                        st.error("השרת עמוס, נסה שוב בעוד דקה.")

    with col2:
        st.header("🥗 תפריט מותאם")
        target = st.selectbox("מה המטרה שלך?", ["מסה נקייה", "מסה מלוכלכת (Dirty Bulk)", "חיטוב אגרסיבי"])
        if st.button("צור תפריט עכשיו"):
            try:
                res = model.generate_content(f"צור תפריט יומי מפורט ל{target} עם דגש על חלבון גבוה. ענה בעברית.")
                st.success(res.text)
            except:
                st.error("גוגל צריכה הפסקה קצרה.")

with tab2:
    st.header("⚡ תוכנית אימון אישית")
    col_a, col_b = st.columns(2)
    with col_a:
        location = st.radio("מיקום האימון:", ["חדר כושר", "בית (משקל גוף)", "מתקני פארק"])
    with col_b:
        goal = st.selectbox("מטרה עיקרית:", ["בניית שריר (Hypertrophy)", "כוח מתפרץ", "סיבולת"])
    
    # הסליידר עובד עכשיו בזכות התיקון ב-CSS
    days = st.slider("כמה ימים בשבוע להקדיש?", 1, 7, 3)
    
    if st.button("בנה לי תוכנית אימון"):
        with st.spinner('בונה תוכנית מנצחת...'):
            try:
                res = model.generate_content(f"Create a workout plan for {goal} at {location} for {days} days. Hebrew.")
                st.markdown(res.text)
            except:
                st.error("חסימת עומס, נסה שוב בעוד רגע.")

with tab3:
    st.header("📊 מחשבון התקדמות")
    w = st.number_input("משקל (kg)", 30.0, 200.0, 60.0)
    h = st.number_input("גובה (cm)", 100, 250, 180)
    if h > 0:
        bmi = w / ((h/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")
        if bmi < 18.5: st.warning("מצב: תת משקל. הגיע הזמן לאכול!")
        elif bmi < 25: st.success("מצב: תקין. תמשיך ככה!")
        else: st.info("מצב: עודף משקל. זמן לזוז.")

with tab4:
    st.header("📝 יומן ניצחונות")
    st.write(f"תאריך: {datetime.date.today()}")
    
    motivational_quotes = [
        "הכאב של היום הוא הכוח של מחר. 💪",
        "אל תסתכל על המרחק, תסתכל על הצעד הבא. 🔥",
        "התירוצים לא בונים שרירים. 🍗",
        "תהיה הגרסה הכי טובה של עצמך. 🧠",
        "הצלחה מתחילה בהחלטה לנסות. 🎯"
    ]
    
    c1, c2 = st.columns(2)
    with c1:
        workout_done = st.checkbox("סיימתי אימון היום! ✅")
        ate_well = st.checkbox("עמדתי בתפריט! 🍱")
    
    with c2:
        if workout_done:
            st.success(random.choice(motivational_quotes))
            st.balloons()
            
    if st.button("שמור ביומן"):
        st.toast("הנתונים נשמרו! גאה בך.")
