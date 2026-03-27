import streamlit as st
import requests
import datetime

# הגדרת המפתח מתוך ה-Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

st.set_page_config(page_title="BodyTrack AI | Pro", layout="wide")

# עיצוב RTL וסגנון כהה
st.markdown("""
    <style>
    .main, .stApp { direction: RTL; text-align: right; background-color: #050a0e; color: white; }
    h1 { color: #00ff88; font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { direction: RTL; }
    .stButton>button { background: linear-gradient(90deg, #00ff88, #00cc66); color: black !important; font-weight: bold; width: 100%; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

def generate_with_api(prompt_text):
    if not API_KEY:
        return "שגיאה: מפתח API חסר ב-Secrets"
    
    # המעקף הסופי: פנייה ישירה לכתובת ה-API הרשמית (v1 ולא v1beta)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"שגיאה בחיבור ל-AI: {str(e)}"

st.title("⚡ BodyTrack AI Pro")
tab1, tab2, tab3, tab4 = st.tabs(["🏋️ תוכנית אימון", "🥗 תפריט", "📊 מדדים", "✅ יומן ניצחונות"])

with tab1:
    st.header("בניית תוכנית אימון")
    location = st.radio("מיקום:", ["חדר כושר", "בית (משקל גוף)", "פארק"])
    goal = st.selectbox("מטרה:", ["בניית שריר", "חיטוב אגרסיבי", "כוח מתפרץ"])
    days = st.slider("ימים בשבוע:", 1, 7, 3)
    if st.button("בנה לי תוכנית"):
        with st.spinner('מייצר תוכנית...'):
            res = generate_with_api(f"Create a workout plan for {goal} at {location} for {days} days. Hebrew.")
            st.markdown(res)

with tab2:
    st.header("🥗 תפריט מותאם")
    target = st.selectbox("מטרה תזונתית:", ["מסה", "חיטוב"])
    if st.button("צור תפריט"):
        with st.spinner('בונה תפריט...'):
            res = generate_with_api(f"צור תפריט יומי ל{target} עם חלבון גבוה. עברית.")
            st.success(res)

with tab3:
    st.header("📊 מחשבון מדדים")
    weight = st.number_input('משקל בק"ג', 30.0, 200.0, 70.0)
    height = st.number_input('גובה בס"מ', 100, 250, 180)
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.metric("ה-BMI שלך", f"{bmi:.1f}")

with tab4:
    st.header("📝 מה עשיתי היום?")
    st.subheader(f"סטטוס ל-{datetime.date.today().strftime('%d/%m/%Y')}")
    col1, col2 = st.columns(2)
    with col1:
        workout = st.checkbox("סימון אימון: בוצע! 🏋️")
    with col2:
        food = st.checkbox("סימון תזונה: אכלתי לפי התפריט! 🍱")
    
    if workout and food:
        st.balloons()
        st.success("יום מושלם! אלוף.")
