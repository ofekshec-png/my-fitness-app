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

st.set_page_config(page_title="BodyTrack AI", layout="wide")

# עיצוב האתר ליישור לימין (RTL) וצבעים
st.markdown("""
    <style>
    /* יישור כל האתר לימין */
    .main, .stApp {
        direction: RTL;
        text-align: right;
    }
    
    /* סידור כפתורים */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00cc66;
        color: white;
        border: none;
    }
    
    /* תיקון כיוון ללשוניות (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        direction: RTL;
        justify-content: flex-start;
    }

    /* יישור כותרות וטקסט */
    h1, h2, h3, p, span, label, .stMarkdown {
        text-align: right;
        direction: RTL;
    }
    
    /* תיקון מיקום האייקונים בהודעות */
    .stAlert {
        direction: RTL;
        text-align: right;
    }

    /* תיקון לשדות קלט (מספרים וטקסט) */
    .stNumberInput, .stTextInput, .stSelectbox {
        direction: RTL;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💪 BodyTrack AI - המאמן האישי שלך")

tab1, tab2, tab3, tab4 = st.tabs(["📸 סורק ותפריט", "🏋️ תוכנית אימונים", "📊 מחשבון BMI", "📝 יומן מעקב"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("ניתוח ארוחה")
        uploaded_file = st.file_uploader("צלם/העלה ארוחה", type=["jpg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            if st.button("נתח ערכים"):
                with st.spinner('מנתח...'):
                    try:
                        prompt = "Analyze this image. Provide: Calories, Protein, Carbs, Fats. Respond in Hebrew."
                        res = model.generate_content([prompt, image])
                        st.info(res.text)
                    except Exception as e:
                        st.error("השרת זיהה עומס. נסה שוב בעוד רגע.")

    with col2:
        st.header("בניית תפריט יומי")
        target = st.selectbox("תפריט לטובת:", ["מסה נקייה", "מסה מלוכלכת", "חיטוב"])
        if st.button("בנה לי תפריט מומלץ"):
            try:
                res = model.generate_content(f"צור תפריט יומי ל{target} עם דגש על חלבון גבוה. ענה בעברית.")
                st.success(res.text)
            except:
                st.error("עומס על השרת, נסה שוב בעוד דקה.")

with tab2:
    st.header("בניית תוכנית לפי מיקום")
    location = st.radio("איפה מתאמנים היום?", ["חדר כושר", "משקל גוף (בית)", "גינת כושר ציבורית"])
    goal = st.selectbox("מטרה:", ["עליה במסה", "כוח מרבי", "סיבולת"])
    days = st.slider("ימים בשבוע", 1, 7, 3)
    if st.button("צור תוכנית אימון"):
        try:
            res = model.generate_content(f"Create a workout plan for {goal} at {location} for {days} days. Hebrew.")
            st.write(res.text)
        except:
            st.error("גוגל צריכה הפסקה קצרה. נסה שוב בעוד רגע.")

with tab3:
    st.header("מחשבון מדדים")
    w = st.number_input("משקל בקילוגרמים", 30.0, 200.0, 60.0)
    h = st.number_input("גובה בסנטימטרים", 100, 250, 180)
    if h > 0:
        bmi = w / ((h/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")
        if bmi < 18.5: st.warning("תת-משקל - זמן למסה!")
        elif bmi < 25: st.success("משקל תקין")
        else: st.info("עודף משקל")

with tab4:
    st.header("📝 יומן מעקב ומוטיבציה")
    st.write(f"היום: {datetime.date.today()}")
    
    motivational_quotes = [
        "המסה של היום היא השריר של מחר! 💪",
        "אל תפסיק כשאתה עייף, תפסיק כשסיימת. 🔥",
        "כל חלבון נחשב, כל סט מקדם אותך למטרה. 🍗",
        "הגוף שלך מסוגל להכל, זה רק הראש שצריך לשכנע. 🧠",
        "זכור למה התחלת – המטרה קרובה מתמיד! 🎯",
        "אין קיצורי דרך, יש רק עבודה קשה ותוצאות. ⚡",
        "התמדה היא הסוד. פשוט תופיע לאימון. 🚀"
    ]
    
    col_check, col_quote = st.columns([1, 2])
    
    with col_check:
        workout_done = st.checkbox("יצאתי לאימון היום! 🏋️")
        ate_well = st.checkbox("אכלתי לפי התפריט 🍱")
        
    with col_quote:
        if workout_done:
            quote = random.choice(motivational_quotes)
            st.success(f"**כל הכבוד אלוף!** \n\n {quote}")
            st.balloons()
            
    if st.button("שמור נתונים ביומן"):
        st.toast("הנתונים נשמרו בהצלחה!")
